import os
import io

from flask import current_app, abort, send_file
from werkzeug.exceptions import BadRequest
from tinydb import Query
import connexion
from openapi_server import util


def annotated_file_path_get(filePath, user=None):  # noqa: E501
    """annotated_file_path_get

    Retrieves an annotated version of the file. # noqa: E501

    :param file_path: Path to file
    :type file_path: str

    :rtype: None
    """

    abs_file_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'], user, filePath)
    if os.path.exists(abs_file_path):
        content = []  # this is memory inefficient but okay for small files.
        lines = connexion.request.headers['Lines'] if 'lines' in connexion.request.headers else None
        if lines:
            lines = lines.split('-')
            if len(lines) != 2:
                raise BadRequest(
                    "Lines should contain two elements, not {}".format(len(lines)))
            elif not len(lines[0]):
                raise BadRequest("You cannot specify a negative number here..")
            elif lines[0] > lines[1]:
                raise BadRequest("Lines should be formatted like start-end")
            elif int(lines[0]) < 1:
                raise BadRequest("Line start cannot be smaller than one")

        with open(abs_file_path, 'r') as file:
            db = util.get_db()
            file_query = Query()
            limit = int(lines[1]) if lines else None

            for ln, line in enumerate(file):
                if lines and ln == limit:
                    break
                if ln == 4:
                    # append definition
                    content.append(
                        '##DESCRIPTION=classification=Classifications by the gchboc task force, seperated using semicolon.\n')
                if line.startswith('#') and not line.startswith('##'):
                    line = line.replace('\n', '\tclassification\n')  # append header
                elif line.startswith('##'):
                    pass
                else:
                    partition = line.partition('\t')
                    chromosome = partition[0]
                    partition = partition[2].partition('\t')
                    start = int(partition[0])
                    end = int(partition[2].partition('\t')[0])
                    ratings = db.search((file_query.name == filePath) & (file_query.chr == chromosome) & (file_query.start == start) & (file_query.end == end))
                    annotation = ';'.join(map(lambda rating: "{}:{}".format(
                        rating["user"], rating["rating"]), ratings)) if len(ratings) else '.'
                    line = line.replace('\n', "\t{}\n".format(annotation))
                content.append(line)
        return send_file(io.BytesIO(''.join(content).encode()),
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
    }, (file_query.name == filePath) & (file_query.chr == chr) & (file_query.start == start) & (file_query.end == end))

    return 'successful'
