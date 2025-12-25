class SecurityConfig:
    # Maximum allowed upload size in bytes (5 MiB)
    MAX_UPLOAD_SIZE = 5 * 1024 * 1024

    # Allowed MIME types for PDF uploads
    ALLOWED_MIME_TYPES = {"application/pdf"}

    # Auto‑delete delay in seconds (1 hour)
    AUTO_DELETE_DELAY = 60 * 60
