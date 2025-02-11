from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from app.keyboards.start_keyboard import get_yes_no_kb

router = Router()  # [1]

class Form(StatesGroup):
    group = State()
    mailing = State()
    mailing_time = State()

@router.message(Command("start"))  # [2]
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Form.group)
    await message.answer(
        "Привет! Я бот расписания УУНиТа. Укажи пожалуйста свою группу. \nПример: ПРО-108б \n(Смотреть расписания других групп, я так же умею)",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Form.group)
async def capture_group(message: Message, state: FSMContext):
    # check group

    await message.answer(
        "Ты хочешь получать рассылки расписания по утрам?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Yes"),
                    KeyboardButton(text="No"),
                ]
            ],
            resize_keyboard=True,
        )
    )

@router.message(F.text.lower() == "нет")
async def answer_no(message: Message):
    await message.answer(
        "Жаль...",
        reply_markup=ReplyKeyboardRemove()
    )