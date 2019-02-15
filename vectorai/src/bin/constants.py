from django.utils import timezone
from django.utils.text import gettext_lazy as _


class Placeholder(object):
    name = "John"
    first_name = "John"
    last_name = "Doe"
    middle_name = "Samantha"
    fullname = "Jane Doe"
    phone = "+44 0000 00000"
    email = "mail@email.com"
    year = timezone.now().year
    website = "https://example.com"

    def __init__(self, country="UK"):
        pass


HTML_MIME_TYPES = [
    {
        "type": "HTML Document",
        "extension": ".html",
        "mime": "text/html",
    },
    {
        "type": "HTML Document",
        "extension": ".htm",
        "mime": "text/html",
    },
]

MEDIA_MIME_TYPES = [
    {
        "type": "Audio File",
        "extension": ".mp3",
        "mime": "audio/mpeg",
    },
    {
        "type": "Audio File",
        "extension": ".mp3",
        "mime": "audio/mp3",
    },
]

PDF_MIME_TYPES = [
    {
        "type": "Adobe PDF",
        "extension": ".pdf",
        "mime": "application/pdf",
    },
]

IMAGE_MIME_TYPES = [
    {
        "type": "Image (PNG)",
        "extension": ".png",
        "mime": "image/png",
    },
    {
        "type": "Image (Jpeg)",
        "extension": ".jpg",
        "mime": "image/jpg",
    },
    {
        "type": "Image (Jpeg)",
        "extension": ".jpeg",
        "mime": "image/jpeg",
    },
    {
        "type": "Image (GIF)",
        "extension": ".gif",
        "mime": "image/gif",
    },
    {
        "type": "Image (TIFF)",
        "extension": ".tiff",
        "mime": "image/tiff",
    },
]

MS_MIME_TYPES = [
    {
        "type": "Microsoft Word Document",
        "extension": ".doc",
        "mime": "application/msword",
    },
    {
        "extension": ".dot",
        "mime": "application/msword",
    },
    {
        "type": "Microsoft Word Document",
        "extension": ".docx",
        "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    },
    {
        "type": "Microsoft Word Document (Template)",
        "extension": ".dotx",
        "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.template",
    },
    {
        "extension": ".docm",
        "mime": "application/vnd.ms-word.document.macroEnabled.12",
    },
    {
        "extension": ".dotm",
        "mime": "application/vnd.ms-word.template.macroEnabled.12",
    },
    {
        "type": "Microsoft Excel",
        "extension": ".xls",
        "mime": "application/vnd.ms-excel",
    },
    {
        "type": "Microsoft Excel",
        "extension": ".xlt",
        "mime": "application/vnd.ms-excel",
    },
    {
        "type": "Microsoft Excel",
        "extension": ".xla",
        "mime": "application/vnd.ms-excel",
    },
    {
        "type": "Microsoft Excel",
        "extension": ".xlsx",
        "mime": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    },
    {
        "type": "Microsoft Excel (Template)",
        "extension": ".xltx",
        "mime": "application/vnd.openxmlformats-officedocument.spreadsheetml.template",
    },
    {
        "extension": ".xlsm",
        "mime": "application/vnd.ms-excel.sheet.macroEnabled.12",
    },
    {
        "extension": ".xltm",
        "mime": "application/vnd.ms-excel.template.macroEnabled.12",
    },
    {
        "extension": ".xlam",
        "mime": "application/vnd.ms-excel.addin.macroEnabled.12",
    },
    {
        "extension": ".xlsb",
        "mime": "application/vnd.ms-excel.sheet.binary.macroEnabled.12",
    },
    {
        "type": "Microsoft Powerpoint",
        "extension": ".ppt",
        "mime": "application/vnd.ms-powerpoint",
    },
    {
        "type": "Microsoft Powerpoint",
        "extension": ".pot",
        "mime": "application/vnd.ms-powerpoint",
    },
    {
        "type": "Microsoft Powerpoint",
        "extension": ".pps",
        "mime": "application/vnd.ms-powerpoint",
    },
    {
        "type": "Microsoft Powerpoint",
        "extension": ".ppa",
        "mime": "application/vnd.ms-powerpoint",
    },
    {
        "type": "Microsoft Powerpoint",
        "extension": ".pptx",
        "mime": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    },
    {
        "type": "Microsoft Powerpoint",
        "extension": ".potx",
        "mime": "application/vnd.openxmlformats-officedocument.presentationml.template",
    },
    {
        "type": "Microsoft Powerpoint",
        "extension": ".ppsx",
        "mime": "application/vnd.openxmlformats-officedocument.presentationml.slideshow",
    },
    {
        "extension": ".ppam",
        "mime": "application/vnd.ms-powerpoint.addin.macroEnabled.12",
    },
    {
        "extension": ".pptm",
        "mime": "application/vnd.ms-powerpoint.presentation.macroEnabled.12",
    },
    {
        "extension": ".potm",
        "mime": "application/vnd.ms-powerpoint.presentation.macroEnabled.12",
    },
    {
        "extension": ".ppsm",
        "mime": "application/vnd.ms-powerpoint.slideshow.macroEnabled.12",
    },
]

MIME_TYPES = PDF_MIME_TYPES + IMAGE_MIME_TYPES + MS_MIME_TYPES + HTML_MIME_TYPES + MEDIA_MIME_TYPES
