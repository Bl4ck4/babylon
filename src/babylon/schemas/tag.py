from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene
from ..database import db_session
from ..models import ModelTag
from ..lib.utils import input_to_dictionary
from flask_jwt_extended import jwt_required


class TagAttributes:
    name = graphene.String(description="Name of tag")


class Tag(SQLAlchemyObjectType, TagAttributes):

    class Meta:
        model = ModelTag
        interfaces = (graphene.relay.Node,)


class CreateTagInput(graphene.InputObjectType, TagAttributes):
    pass


class CreateTag(graphene.Mutation):
    tag = graphene.Field(lambda: Tag, description="Tag created by this mutation")

    class Arguments:
        input = CreateTagInput(required=True)

    @jwt_required
    def mutate(self, info, input):
        data = input_to_dictionary(input)

        tag = ModelTag(**data)
        db_session.add(tag)
        db_session.commit()

        return CreateTag(tag=tag)


class UpdateTagInput(graphene.InputObjectType, TagAttributes):
    id = graphene.ID(required=True, description="Global ID of the tag")


class UpdateTag(graphene.Mutation):
    tag = graphene.Field(lambda: Tag, description="Tag updated by this mutation")

    class Arguments:
        input = UpdateTagInput(required=True)

    @jwt_required
    def mutate(self, info, input):
        data = input_to_dictionary(input)

        tag = db_session.query(ModelTag).filter_by(id=data['id'])
        tag.update(data)
        db_session.commit()
        tag = db_session.query(ModelTag).filter_by(id=data['id']).first()
        return UpdateTag(tag=tag)
