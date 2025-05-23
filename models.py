""" Models of used JSON messages """
from marshmallow import Schema, fields, validate
from marshmallow.decorators import validates_schema

class ConfigurationContainerSchema(Schema):
    # TODO: document defaults in documentation-repo 
    # there are inconsistencies between computation and computation template
    # TODO: write more validators, e.g. for regex-pattern or image
    command_line_arguments = fields.String(data_key="running.commandLineArguments",
                                           load_default=None)
    entrypoint = fields.String(data_key="running.entrypoint", load_default=None)
    intermediate_files_pattern = \
        fields.List(fields.String, data_key="running.intermediateFilesPattern", load_default=[])
    image = fields.String(data_key="resources.image", required=True)
    volume = fields.String(data_key="resources.volume", load_default=None)
    memory = fields.String(data_key="resources.memory", load_default='64mb')
    num_cpus = fields.Integer(data_key="resources.numCPUs", load_default=1)
    output = fields.List(fields.Raw(required=False))

class PartSchema(Schema):
    identifier = fields.UUID(required=True)
    access = fields.String(required=True,
                           validate=validate.OneOf(["invisible", "visible", 
                                                    "modifiable", "template"]))
    content = fields.String(load_default="")
    # TODO: bug in websocket-api: should be removed
    metadata = fields.Raw()

class FileSchema(Schema):
    identifier = fields.UUID(required=True)
    path = fields.String(required=True)
    parts = fields.List(fields.Nested(PartSchema), required=True)
    
class ComputationSchema(Schema):
    identifier = fields.UUID(required=True)
    environment = fields.String(required=True,
                                validate=validate.OneOf(["Container", "C", 
                                                         "C++", "Java", 
                                                         "Matlab", "Octave", 
                                                         "DuMuX"]))
    files = fields.List(fields.Nested(FileSchema), required=True)
    configuration = fields.Raw(required=True)

    @validates_schema
    def validate_configuration(self, data, **kwargs):
        if data["environment"] == "Container":
            ConfigurationContainerSchema().validate(data["configuration"])
