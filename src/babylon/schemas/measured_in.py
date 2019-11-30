from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene
from ..database import db_session
from ..models import ModelMeasuredIn
from ..lib.utils import input_to_dictionary
from flask_jwt_extended import jwt_required

class MeasuredInAttributes:
    measurement = graphene.String(description="Which format is this measured in")


class MeasuredIn(SQLAlchemyObjectType, MeasuredInAttributes):

    class Meta:
        model = ModelMeasuredIn
        interfaces = (graphene.relay.Node,)


class CreateMeasuredInInput(graphene.InputObjectType, MeasuredInAttributes):
    pass


class CreateMeasuredIn(graphene.Mutation):
    measured_in = graphene.Field(lambda: MeasuredIn, description="MeasuredIn created by this mutation")

    class Arguments:
        input = CreateMeasuredInInput(required=True)

    @jwt_required
    def mutate(self, info, input):
        data = input_to_dictionary(input)

        measured_in = ModelMeasuredIn(**data)
        db_session.add(measured_in)
        db_session.commit()
        return CreateMeasuredIn(measured_in=measured_in)


class UpdateMeasuredInInput(graphene.InputObjectType, MeasuredInAttributes):
    id = graphene.ID(required=True, description="Global ID of the measured_in")


class UpdateMeasuredIn(graphene.Mutation):
    measured_in = graphene.Field(lambda: MeasuredIn, description="MeasuredIn updated by this mutation")

    class Arguments:
        input = UpdateMeasuredInInput(required=True)

    @jwt_required
    def mutate(self, info, input):
        data = input_to_dictionary(input)

        measured_in = db_session.query(ModelMeasuredIn).filter_by(id=data["id"])
        measured_in.update(data)
        db_session.commit()
        measured_in = db_session.query(ModelMeasuredIn).filter_by(id=data["id"]).first()
        return UpdateMeasuredIn(measured_in=measured_in)