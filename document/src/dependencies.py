import uuid

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from src.rabbitMq.hospital import RabbitMQClient as hospitalRoomRPC
from src.rabbitMq.token import RabbitMQClient as tokenRPC
from src.rabbitMq.doctor import RabbitMQClient as doctorRPC
from src.rabbitMq.pacient import RabbitMQClient as pacientRPC

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8081/api/Authentication/SignIn")


async def validate_token(token: str = Depends(oauth2_scheme)):
    rabbitmq = tokenRPC()
    response: bool | str = await rabbitmq.call(token)
    if response is True:
        return token
    else:
        raise HTTPException(status_code=401, detail=response)


async def get_current_user(token: str = Depends(validate_token)):
    decoded = jwt.decode(
        token, options={"verify_signature": False}
    )
    return decoded


def validate_user_role(allowed_roles: list):
    async def role_dependency(user: dict = Depends(get_current_user)):
        if not any(role in allowed_roles for role in user.get('roles')):
            raise HTTPException(status_code=403, detail="Not enough privileges.")
        return user
    return role_dependency


async def validate_room_hospital(hospital_id: uuid.UUID, room: str):
    hospital_client = hospitalRoomRPC()
    exist_room = await hospital_client.call_room(hospital_id, room)

    if exist_room is not True:
        raise HTTPException(status_code=404, detail=exist_room)
    return True


async def validate_pacient(pacient_id: uuid.UUID):
    pacient_client = pacientRPC()
    exist_pacient = await pacient_client.call(pacient_id)

    if not exist_pacient:
        raise HTTPException(status_code=404, detail='Pacient not found.')
    return True


async def validate_doctor(doctor_id: uuid.UUID):
    doctor_client = doctorRPC()
    exist_doctor = await doctor_client.call(doctor_id)

    if not exist_doctor:
        raise HTTPException(status_code=404, detail='Doctor not found.')
    return True
