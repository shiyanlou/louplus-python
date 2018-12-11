from marshmallow import Schema, fields


class FileSchema(Schema):
    _id = fields.Str()
    filename = fields.Str()
    content_type = fields.Str()
    length = fields.Int()
    chunk_size = fields.Int()
    upload_date = fields.DateTime()
    aliases = fields.Str()
    metadata = fields.Dict()
    md5 = fields.Str()
