import os
import uuid
from flask import current_app


class StorageService:
    """
    Serviço de upload/delete de arquivos.
    Tenta Supabase Storage primeiro; usa fallback local se indisponível.

    Buckets / subpastas:
      - 'exclusive-covers' → coleção exclusiva
      - 'lancamentos'      → capas e galeria de lançamentos
    """

    BUCKET_EXCLUSIVE   = 'exclusive-covers'
    BUCKET_LANCAMENTOS = 'lancamentos'

    # Caminho base dentro de app/static para fallback local
    LOCAL_BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'uploads')

    # ── Cliente Supabase ──────────────────────────────────────────────────

    @classmethod
    def _client(cls):
        from supabase import create_client
        url = os.getenv('SUPABASE_URL') or current_app.config.get('SUPABASE_URL', '')
        key = (os.getenv('SUPABASE_SERVICE_KEY')
               or os.getenv('SUPABASE_KEY')
               or current_app.config.get('SUPABASE_KEY', ''))
        if not url or not key:
            raise ValueError("SUPABASE_URL/SUPABASE_KEY não configurados")
        return create_client(url, key)

    # ── Upload genérico com fallback local ────────────────────────────────

    @classmethod
    def _upload(cls, bucket: str, path: str, file_bytes: bytes, content_type: str) -> str:
        """
        Faz upload para Supabase Storage.
        Em caso de falha, salva localmente em app/static/uploads/<bucket>/<path>
        e retorna a URL estática do Flask.
        """
        try:
            client = cls._client()
            try:
                client.storage.from_(bucket).remove([path])
            except Exception:
                pass
            client.storage.from_(bucket).upload(
                path=path,
                file=file_bytes,
                file_options={"content-type": content_type, "upsert": "true"}
            )
            supabase_url = os.getenv('SUPABASE_URL') or current_app.config.get('SUPABASE_URL', '')
            return f"{supabase_url}/storage/v1/object/public/{bucket}/{path}"

        except Exception as e:
            current_app.logger.warning(f"[Storage] Supabase falhou ({e}), usando armazenamento local.")
            return cls._save_local(bucket, path, file_bytes)

    @classmethod
    def _save_local(cls, bucket: str, path: str, file_bytes: bytes) -> str:
        """Salva arquivo localmente e retorna URL estática Flask."""
        # Monta caminho: app/static/uploads/<bucket>/<path>
        dest = os.path.join(cls.LOCAL_BASE, bucket, path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'wb') as f:
            f.write(file_bytes)
        # Retorna URL relativa ao static
        rel = f"uploads/{bucket}/{path}".replace("\\", "/")
        return f"/static/{rel}"

    # ── Delete genérico ───────────────────────────────────────────────────

    @classmethod
    def delete_file(cls, url: str, bucket: str):
        """Remove arquivo do Supabase ou do sistema local."""
        if not url:
            return
        # Arquivo local
        if url.startswith('/static/uploads/'):
            try:
                # Remove o prefixo /static/uploads/ para obter o path relativo
                rel = url[len('/static/uploads/'):]
                full = os.path.join(cls.LOCAL_BASE, rel)
                if os.path.exists(full):
                    os.remove(full)
            except Exception as e:
                current_app.logger.warning(f"[Storage] Erro ao deletar local {url}: {e}")
            return
        # Arquivo Supabase
        try:
            marker = f"/object/public/{bucket}/"
            if marker in url:
                file_path = url.split(marker)[-1]
                client = cls._client()
                client.storage.from_(bucket).remove([file_path])
        except Exception as e:
            current_app.logger.warning(f"[Storage] Erro ao deletar Supabase {url}: {e}")

    # ── Coleção Exclusiva ─────────────────────────────────────────────────

    @classmethod
    def upload_cover(cls, file_bytes: bytes, filename: str, content_type: str = 'image/jpeg') -> str:
        """Upload de capa para o bucket exclusive-covers."""
        return cls._upload(cls.BUCKET_EXCLUSIVE, f"covers/{filename}", file_bytes, content_type)

    @classmethod
    def delete_cover(cls, cover_url: str):
        """Remove capa do bucket exclusive-covers."""
        cls.delete_file(cover_url, cls.BUCKET_EXCLUSIVE)

    # ── Lançamentos ───────────────────────────────────────────────────────

    @classmethod
    def upload_lancamento_cover(cls, file_bytes: bytes, filename: str, content_type: str = 'image/jpeg') -> str:
        """Upload de capa vertical (3:5) de lançamento."""
        return cls._upload(cls.BUCKET_LANCAMENTOS, f"covers/{filename}", file_bytes, content_type)

    @classmethod
    def upload_lancamento_image(cls, file_bytes: bytes, filename: str, content_type: str = 'image/jpeg') -> str:
        """Upload de imagem da galeria de lançamento."""
        return cls._upload(cls.BUCKET_LANCAMENTOS, f"gallery/{filename}", file_bytes, content_type)

    @classmethod
    def delete_lancamento_file(cls, url: str):
        """Remove qualquer arquivo do bucket lancamentos."""
        cls.delete_file(url, cls.BUCKET_LANCAMENTOS)


