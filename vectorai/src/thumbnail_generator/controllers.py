import json
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .bin import debug_logger


# For the purpose of this exercise we will use very simple function based view as against
# class views which are more sophisticated


@require_http_methods(["POST"])
@csrf_exempt
def generate(request):
    """
    This controller handles incoming files from the frontend app and returns JSON content
    containing the folder_name (used to access the tmp generated thumbnails) and an array of the
    PDF page grouping

    :param request:
    :return:
    """
    from .bin import extract_pdf_thumbnails, group_randomizer_factory

    # retrieve files from the request object
    _file = request.FILES.get("pdf_file")

    # retrieve a folder name and page number for this file
    folder_name, page_number = extract_pdf_thumbnails(_file)

    # generate a randomize grouping of the file in 3  distinct groups
    pdf_document_group = group_randomizer_factory(page_number, 3)

    # process data in json and return to front end
    json_response_object = {
        "folder_name": folder_name,
        "pdf_document_group": pdf_document_group,
    }

    response = json.dumps(json_response_object)

    return HttpResponse(response, content_type='application/json')


@require_http_methods(["POST"])
@csrf_exempt
def rearrange(request):
    """
    This controller function handles an incoming array grouping from the frontend and
    generates a separate file for each group
    :param request:
    :return:
    """
    from PyPDF2 import PdfFileWriter, PdfFileReader

    # extract request data from the frontend
    r = json.loads(request.body.decode("utf-8"))
    arrangements = r["arrangement"]
    folder_name = r["folderName"]

    main_document = PdfFileReader(open("%s/%s/_main.pdf" % (settings.BASE_DIR, folder_name), 'rb'))

    # initialize the document labels
    document_labels = ["alpha", "beta", "gamma"]
    outputs = list()

    # process new documents into separate files and send back to the frontend for download
    k = 0
    for document_label in document_labels:
        tmp_document = PdfFileWriter()

        for page_num in arrangements[k]:
            tmp_document.addPage(main_document.getPage(page_num))

        filename = '%s/%s/%s.pdf' % (settings.BASE_DIR, folder_name, document_label)

        with open(filename, 'wb') as f:
            tmp_document.write(f)

        outputs.append({
            "download_link": "%s/%s/%s.pdf" % (settings.BASE_URL, folder_name, document_label),
            "filename": document_label.title(),
        })

        k += 1

    return HttpResponse(json.dumps({"downloads": outputs}), content_type='application/json')


@require_http_methods(["GET"])
@csrf_exempt
def home(request):
    """
    Home page view
    :param request:
    :return:
    """
    # todo: you may wish to remove soonest, a redundant view
    return HttpResponse('Vector ai home page')
