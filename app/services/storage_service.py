import os
import uuid
import boto3
from botocore.exceptions import ClientError
from flask import current_app


class StorageService:
    """
    Serviço de upload/delete de arquivos via Cloudflare R2 (API S3 compatível).
    Usa fallback local em app/static/uploads se as credenciais R2 falharem ou não estiverem configuradas.

    Buckets / subpastas lógicas:
      - 'exclusive-covers' → coleção exclusiva
      - 'lancamentos'      → capas e galeria de lançamentos
      - 'agents'           → avatares de corretores
    """

    # Mantemos a mesma assinatura do antigo Supabase para não quebrar o código
    BUCKET_EXCLUSIVE   = 'exclusive-covers'
    BUCKET_LANCAMENTOS = 'lancamentos'
    BUCKET_AGENTS      = 'agents'

    # Caminho base dentro de app/static para fallback local
    LOCAL_BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'uploads')

    # ── Cliente Cloudflare R2 ─────────────────────────────────────────────

    @classmethod
    def _client(cls):
        account_id = os.getenv('R2_ACCOUNT_ID') or current_app.config.get('R2_ACCOUNT_ID', '')
        access_key = os.getenv('R2_ACCESS_KEY_ID') or current_app.config.get('R2_ACCESS_KEY_ID', '')
        secret_key = os.getenv('R2_SECRET_ACCESS_KEY') or current_app.config.get('R2_SECRET_ACCESS_KEY', '')
        
        if not account_id or not access_key or not secret_key:
            raise ValueError("Credenciais R2 (R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY) não configuradas.")
            
        endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"
        
        return boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='auto'  # R2 exige 'auto' ou us-east-1
        )
        
    @classmethod
    def _get_bucket_name(cls):
        # Todos os subdiretórios (agents, lancamentos) vão para dentro de um único bucket no R2.
        # Defina R2_BUCKET_NAME no .env
        return os.getenv('R2_BUCKET_NAME') or current_app.config.get('R2_BUCKET_NAME', '7x-imoveis')

    @classmethod
    def _get_public_url(cls, key: str) -> str:
        # A URL pública configurada no Cloudflare (ex: https://pub-xxxx.r2.dev ou seu domínio proprio)
        public_url = (os.getenv('R2_PUBLIC_URL') or current_app.config.get('R2_PUBLIC_URL', '')).rstrip('/')
        if not public_url:
            # Fallback (não ideal, o R2 precisa de domínio público)
            bucket = cls._get_bucket_name()
            account_id = os.getenv('R2_ACCOUNT_ID') or ''
            return f"https://{account_id}.r2.cloudflarestorage.com/{bucket}/{key}"
        return f"{public_url}/{key}"

    # ── Upload genérico com fallback local ────────────────────────────────

    @classmethod
    def _upload(cls, folder: str, path: str, file_bytes: bytes, content_type: str) -> str:
        """
        Faz upload para Cloudflare R2 usando boto3.
        Em caso de falha, salva localmente em app/static/uploads/<folder>/<path>
        e retorna a URL estática do Flask.
        """
        key = f"{folder}/{path}"
        try:
            client = cls._client()
            bucket_name = cls._get_bucket_name()
            
            # S3 API upload
            client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=file_bytes,
                ContentType=content_type
            )
            
            return cls._get_public_url(key)

        except Exception as e:
            current_app.logger.warning(f"[Storage] R2 Upload falhou ({e}), usando armazenamento local.")
            return cls._save_local(folder, path, file_bytes)

    @classmethod
    def _save_local(cls, folder: str, path: str, file_bytes: bytes) -> str:
        """Salva arquivo localmente e retorna URL estática Flask."""
        dest = os.path.join(cls.LOCAL_BASE, folder, path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'wb') as f:
            f.write(file_bytes)
        rel = f"uploads/{folder}/{path}".replace("\\", "/")
        return f"/static/{rel}"

    # ── Delete genérico ───────────────────────────────────────────────────

    @classmethod
    def delete_file(cls, url: str, folder: str):
        """Remove arquivo do R2 ou do sistema local."""
        if not url:
            return
            
        # Arquivo local
        if url.startswith('/static/uploads/'):
            try:
                rel = url[len('/static/uploads/'):]
                full = os.path.join(cls.LOCAL_BASE, rel)
                if os.path.exists(full):
                    os.remove(full)
            except Exception as e:
                current_app.logger.warning(f"[Storage] Erro ao deletar local {url}: {e}")
            return
            
        # Arquivo R2
        try:
            public_url = (os.getenv('R2_PUBLIC_URL') or current_app.config.get('R2_PUBLIC_URL', '')).rstrip('/')
            if public_url and url.startswith(public_url):
                key = url[len(public_url) + 1:]
            else:
                # Tenta extrair a chave se for URL padrão do endpoint (fallback)
                key = url.split('.cloudflarestorage.com/')[-1]
                if '/' in key:
                    # Remove o nome do bucket do inicio se houver
                    bucket = cls._get_bucket_name()
                    if key.startswith(f"{bucket}/"):
                        key = key[len(bucket) + 1:]
                        
            client = cls._client()
            client.delete_object(
                Bucket=cls._get_bucket_name(),
                Key=key
            )
        except Exception as e:
            current_app.logger.warning(f"[Storage] Erro ao deletar R2 {url}: {e}")

    # ── Coleção Exclusiva ─────────────────────────────────────────────────

    @classmethod
    def upload_cover(cls, file_bytes: bytes, filename: str, content_type: str = 'image/jpeg') -> str:
        return cls._upload(cls.BUCKET_EXCLUSIVE, f"covers/{filename}", file_bytes, content_type)

    @classmethod
    def delete_cover(cls, cover_url: str):
        cls.delete_file(cover_url, cls.BUCKET_EXCLUSIVE)

    # ── Lançamentos ───────────────────────────────────────────────────────

    @classmethod
    def upload_lancamento_cover(cls, file_bytes: bytes, filename: str, content_type: str = 'image/jpeg') -> str:
        return cls._upload(cls.BUCKET_LANCAMENTOS, f"covers/{filename}", file_bytes, content_type)

    @classmethod
    def upload_lancamento_image(cls, file_bytes: bytes, filename: str, content_type: str = 'image/jpeg') -> str:
        return cls._upload(cls.BUCKET_LANCAMENTOS, f"gallery/{filename}", file_bytes, content_type)

    @classmethod
    def delete_lancamento_file(cls, url: str):
        cls.delete_file(url, cls.BUCKET_LANCAMENTOS)

    # ── Corretores (Agentes) ──────────────────────────────────────────────

    @classmethod
    def upload_agent_avatar(cls, file_bytes: bytes, filename: str, content_type: str = 'image/jpeg') -> str:
        return cls._upload(cls.BUCKET_AGENTS, f"avatars/{filename}", file_bytes, content_type)

    @classmethod
    def delete_agent_avatar(cls, url: str):
        cls.delete_file(url, cls.BUCKET_AGENTS)

