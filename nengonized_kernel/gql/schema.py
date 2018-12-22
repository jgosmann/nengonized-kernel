import traceback

from graphene import (
        Field, List, Int, Mutation, NonNull, ObjectType, Schema, String)

from .nengo_model_schema import Network
from ..model_loader import (
        ExecutionError, ModelLoader, ModelNotFoundError)


class Context(object):
    def __init__(self, model=None, errors=None):
        self.model = model
        self.errors = errors


class FrameSummary(ObjectType):
    filename = String()
    lineno = Int()
    name = String()

    @classmethod
    def from_obj(cls, obj):
        return cls(filename=obj.filename, lineno=obj.lineno, name=obj.name)


class Error(ObjectType):
    type = None # TODO
    message = NonNull(String)
    traceback = List(NonNull(FrameSummary))
    filename = String()
    lineno = Int()
    offset = Int()
    text = String()

    @classmethod
    def from_exception(cls, err):
        if isinstance(err, ExecutionError):
            if isinstance(err.inner_exception, SyntaxError):
                return cls._from_syntax_error(err.inner_exception)
            else:
                return cls._from_inner_execution_error(err.inner_exception)
        else:
            return cls._from_general_error(err)

    @classmethod
    def _from_inner_execution_error(cls, err):
        tb = [FrameSummary.from_obj(f)
              for f in traceback.extract_tb(err.__traceback__)]
        return Error(
                message=str(err),
                traceback=tb[1:],
                filename=tb[1].filename,
                lineno=tb[1].lineno)

    @classmethod
    def _from_syntax_error(cls, err):
        return Error(
                message=str(err),
                filename=err.filename,
                lineno=err.lineno,
                offset=err.offset,
                text=err.text)

    @classmethod
    def _from_general_error(cls, err):
        return Error(
            message=str(err),
            traceback=[
                FrameSummary.from_obj(f)
                for f in traceback.extract_tb(err.__traceback__)
            ]
        )


class RootQuery(ObjectType):
    model = Field(Network)
    errors = List(NonNull(Error))

    def resolve_model(self, info):
        return Network(info.context.model)

    def resolve_errors(self, info):
        if info.context.errors is None:
            return []
        return [Error.from_exception(err) for err in info.context.errors]


schema = Schema(query=RootQuery)
