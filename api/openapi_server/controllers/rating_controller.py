import os
import io

from flask import current_app, abort, send_file
from tinydb import Query

from openapi_server import util


def annotated_file_path_get(filePath, user=None):  # noqa: E501
    """annotated_file_path_get

    Retrieves an annotated version of the file. # noqa: E501

    :param file_path: Path to file
    :type file_path: str

    :rtype: None
    """

    abs_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], user, filePath)
    if os.path.exists(abs_file_path):
        db = util.get_db()
        file_query = Query()
        lines = [] # this is memory inefficient but okay for small files.

        with open(abs_file_path, 'r') as file:
            for ln, line in enumerate(file):
                if ln == 4:
                    lines.append('##DESCRIPTION=gchboc=Annotations by the gchboc task force, seperated using semicolon.\n') # append definition
                if line.startswith('#') and not line.startswith('##'):
                    line = line.rstrip() + '\tgchboc\n' # append header
                else:
                    partition = line.partition('\t')
                    chromosome = partition[0]
                    partition = partition[2].partition('\t')
                    start = partition[0]
                    end = partition[2].partition('\t')[0]
                    ratings = db.search((file_query.name == filePath) & (file_query.chr == chromosome)
                                        & (file_query.start == start) & (file_query.end == end))
                    annotation = ';'.join(map(lambda rating: rating['rating'], ratings)) if len(ratings) else '.'
                    line = line.rstrip() + "\t{}\n".format(annotation)
                lines.append(line)

        return send_file(io.BytesIO(''.join(lines).encode()),
                         attachment_filename=filePath,
                         as_attachment=True)
    else:
        abort(404)


def rate_put(filePath, chr, start, end, rating, user=None):  # noqa: E501
    """rate_file_path_chr_start_end_rating_put

    Rate a file. This uses JWT to verify the user. # noqa: E501

    :param file_path: Path to file
    :type file_path: str
    :param chr: The chromosome to rate for
    :type chr: str
    :param start: The start position to rate for
    :type start:
    :param end: The end position to annotate for
    :type end:
    :param rating: Which rating this variant should have.
    :type rating:

    :rtype: None
    """
    db = util.get_db()
    file_query = Query()
    db.upsert({
        'name': filePath,
        'chr': chr,
        'start': start,
        'end': end,
        'rating': rating,
        'user': user
    }, file_query.name == filePath)

    return 'successful'
