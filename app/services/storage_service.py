import os
from flask import current_app


class StorageService:
    """
    Serviço de upload/delete de arquivos no Supabase Storage.
    Bucket padrão: 'exclusive-covers'
    """

    BUCKET = 'exclusive-covers'

    @classmethod
    def _client(cls):
        from supabase import create_client
        url = os.getenv('SUPABASE_URL') or current_app.config.get('SUPABASE_URL', '')
        # Usa a Service Role key para operações de admin (upload/delete no Storage)
        # Fallback para a chave pública se não tiver a service key
        key = (os.getenv('SUPABASE_SERVICE_KEY')
               or os.getenv('SUPABASE_KEY')
               or current_app.config.get('SUPABASE_KEY', ''))
        if not url or not key:
            raise ValueError("SUPABASE_URL e SUPABASE_SERVICE_KEY devem estar configurados no .env")
        return create_client(url, key)

    @classmethod
    def upload_cover(cls, file_bytes: bytes, filename: str, content_type: str = 'image/jpeg') -> str:
        """
        Faz upload de uma imagem para o bucket 'exclusive-covers'.
        Retorna a URL pública do arquivo.
        """
        client = cls._client()
        path = f"covers/{filename}"

        # Deleta se já existir (upsert manual)
        try:
            client.storage.from_(cls.BUCKET).remove([path])
        except Exception:
            pass

        client.storage.from_(cls.BUCKET).upload(
            path=path,
            file=file_bytes,
            file_options={"content-type": content_type, "upsert": "true"}
        )

        # Monta a URL pública
        supabase_url = os.getenv('SUPABASE_URL') or current_app.config.get('SUPABASE_URL', '')
        public_url = f"{supabase_url}/storage/v1/object/public/{cls.BUCKET}/{path}"
        return public_url

    @classmethod
    def delete_cover(cls, cover_url: str):
        """
        Remove um arquivo do Supabase Storage a partir da URL pública.
        """
        if not cover_url:
            return
        try:
            # Extrai o path do arquivo da URL
            marker = f"/object/public/{cls.BUCKET}/"
            if marker in cover_url:
                file_path = cover_url.split(marker)[-1]
                client = cls._client()
                client.storage.from_(cls.BUCKET).remove([file_path])
        except Exception as e:
            current_app.logger.warning(f"[Storage] Erro ao deletar {cover_url}: {e}")
