from sqlmodel import Session

from models import Chat, Message
from repos.chat import ChatsRepository
from repos.deal import DealsRepository
from repos.user import UsersRepository
from schemas.chat import ChatBase, ChatCreate, MessageBase, MessageCreate


class ChatsService:
    def __init__(self, session: Session):
        self.session = session
        self.chats_repo = ChatsRepository(session)
        self.users_repo = UsersRepository(session)
        self.deals_repo = DealsRepository(session)


    def list_chats(self) -> list[Chat]:
        return self.chats_repo.list()

    def get_chat(self, chat_id: int, user_id: int) -> Chat:
        chat = self.chats_repo.get(chat_id)
        if not chat:
            raise LookupError("Chat not found")

        if not self.chats_repo.is_participant(chat_id=chat_id, user_id=user_id):
            raise PermissionError("You are not a participant of this chat")

        return chat

    def create_chat(self, payload: ChatCreate, user_id: int) -> Chat:
        participant_ids = list(set(payload.participant_ids))
        if len(participant_ids) != 2:
            raise ValueError("Chat can be created for two different users")

        u1, u2 = participant_ids

        if not self.users_repo.get(u1) or not self.users_repo.get(u2):
            raise LookupError("User not found")

        if user_id not in participant_ids:
            raise PermissionError("You are not a participant of this chat")

        existing_chat_id = self.chats_repo.find_chat_id_for_two_users(u1, u2)
        if existing_chat_id:
            raise ValueError("Chat already exists for these participants")

        chat = Chat(title=payload.title)
        self.chats_repo.add(chat)
        self.chats_repo.commit()
        self.chats_repo.refresh(chat)

        for user_id in participant_ids:
            self.chats_repo.add_participant(chat_id=chat.id, user_id=user_id)

        self.chats_repo.commit()
        self.chats_repo.refresh(chat)

        return chat

    def delete_chat(self, chat_id: int, user_id: int) -> None:
        chat = self.chats_repo.get(chat_id)
        if not chat:
            raise LookupError("Chat not found")
        if not self.chats_repo.is_participant(chat_id=chat_id, user_id=user_id):
            raise PermissionError("You are not a participant of this chat")

        self.chats_repo.delete(chat)
        self.chats_repo.commit()

    def update_chat(self, chat_id: int, payload: ChatBase, user_id: int) -> Chat:
        chat = self.chats_repo.get(chat_id)
        if not chat:
            raise LookupError("Chat not found")

        if not self.chats_repo.is_participant(chat_id=chat_id, user_id=user_id):
            raise PermissionError("You are not a participant of this chat")

        data = payload.model_dump(mode="json", exclude_unset=True)
        for k, v in data.items():
            setattr(chat, k, v)

        self.chats_repo.add(chat)
        self.chats_repo.commit()
        self.chats_repo.refresh(chat)
        return chat


    def list_messages(self, chat_id: int, user_id: int) -> list[Message]:
        if not self.chats_repo.get(chat_id):
            raise LookupError("Chat not found")
        if not self.chats_repo.is_participant(chat_id=chat_id, user_id=user_id):
            raise PermissionError("You are not a participant of this chat")

        return self.chats_repo.list_messages(chat_id)

    def get_message(self, message_id: int, user_id: int) -> Message:
        msg = self.chats_repo.get_message(message_id)
        if not msg:
            raise LookupError("Message not found")
        if not self.chats_repo.is_participant(chat_id=msg.chat_id, user_id=user_id):
            raise PermissionError("User is not a participant of this chat")
        return msg

    def create_message(self, payload: MessageCreate, user_id: int) -> Message:
        chat = self.chats_repo.get(payload.chat_id)
        if not chat:
            raise LookupError("Chat not found")

        if not self.chats_repo.is_participant(chat_id=payload.chat_id, user_id=user_id):
            raise PermissionError("User is not a participant of this chat")

        data = payload.model_dump(mode="json")
        msg = Message(**data, sender_id=user_id)

        self.chats_repo.add_message(msg)
        self.chats_repo.commit()
        self.chats_repo.refresh(msg)
        return msg

    def delete_message(self, message_id: int, user_id: int) -> None:
        msg = self.chats_repo.get_message(message_id)
        if not msg:
            raise LookupError("Message not found")
        if not self.chats_repo.is_participant(chat_id=msg.chat_id, user_id=user_id):
            raise PermissionError("User is not a participant of this chat")

        self.session.delete(msg)
        self.chats_repo.commit()

    def update_message(self, message_id: int, payload: MessageBase, user_id: int) -> Message:
        msg = self.chats_repo.get_message(message_id)
        if not msg:
            raise LookupError("Message not found")
        if msg.sender_id != user_id:
            raise PermissionError("User is not a participant of this chat")

        data = payload.model_dump(mode="json", exclude_unset=True)
        for k, v in data.items():
            setattr(msg, k, v)

        self.chats_repo.add_message(msg)
        self.chats_repo.commit()
        self.chats_repo.refresh(msg)
        return msg

    def list_user_chats(self, user_id: int) -> list[Chat]:
        if not self.users_repo.get(user_id):
            raise LookupError("User not found")
        return self.chats_repo.list_user_chats(user_id)

    def list_user_deals(self, user_id: int):
        if not self.users_repo.get(user_id):
            raise LookupError("User not found")
        return self.deals_repo.list_for_user_detail(user_id)