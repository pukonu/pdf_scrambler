from django.conf import settings


def extract_pdf_thumbnails(f):
    """
    An extractor to extract the thumbnails from a specified pdf file
    this function will also keep the original copy of the pdf file passed
    :param f:
    :return:
    """

    import os
    from django.utils.text import slugify
    from PyPDF2 import PdfFileReader
    from wand.image import Image

    # generate a folder name we'd use to store all generated files for this transaction
    tmp_folder_name = "media/%s" % slugify(f.name.split(".")[0])

    # extract the thumbnails for this file using ImageMagick, python's wand library will be our broker
    if not os.path.exists(tmp_folder_name):
        os.mkdir(tmp_folder_name)

        try:
            with Image(file=f, resolution=150) as img:
                img.compression_quality = 80
                img.save(filename="%s/%s/tmp.jpg" % (settings.BASE_DIR, tmp_folder_name))

        except Exception as exp:
            debug_logger(exp)

    # write file into a temporary folder
    # todo: production build use a persistent storage like S3 using boto3
    handle_uploaded_file(f, "%s/%s/_main.pdf" % (settings.BASE_DIR, tmp_folder_name))

    # return a tuple of the temporary folder name and number of pages in the file
    return tmp_folder_name, PdfFileReader(f).getNumPages()


def group_randomizer_factory(arr, groups):
    from random import shuffle

    arr = range(arr)

    # will do some shuffling to randomize the page order
    arr = [x for x in arr]
    shuffle(arr)
    ret = []
    group_size = 1.0 / groups * len(arr)

    # will now break the array into equal sizes from the middle of length of array parsed
    for i in range(groups):
        ret.append(arr[int(round(i * group_size)):int(round((i + 1) * group_size))])

    return ret


def handle_uploaded_file(f, filename):
    """
    This is where we will handle files to be uploaded, ideally in production we'd use a persistent storage
    like Amazon's S3 (boto3) rather than this volatile one, although it will do for this sample app.
    :param f:
    :param filename:
    :return:
    """
    # todo: Depending on the file size we will queue this request using Celery (will check for files > 2MB)

    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def debug_logger(v):
    """
    Just a simple function to log the errors
    :param v:
    :return:
    """
    # todo: for production change to a more sophisticated error logger
    f = open("debug.log", "a")
    f.write("%s\n" % v)
    f.close()
