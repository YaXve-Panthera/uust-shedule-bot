from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from app.keyboards.start_keyboard import get_yes_no_kb, get_mailing_type
from app.services.validate import group_name_validate

router = Router()  # [1]

class Form(StatesGroup):
    group = State()
    mailing = State()
    mailing_type = State()
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
    if await group_name_validate(message.text):
        await state.set_state(Form.mailing)
        await state.update_data(group=message.text)
        await message.answer(
            "Ты хочешь получать рассылки расписания по утрам?",
            reply_markup=get_yes_no_kb()
        )
    else:
        await message.answer(
            "Вы или ввели не верное название группы, или такой группы не существует",
            reply_markup=ReplyKeyboardRemove()
        )

@router.message(F.text.lower() == "Нет", Form.mailing)
async def mailing_answer_no(message: Message):
    await message.answer(
        "Жаль...",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text.lower() == "да", Form.mailing)
async def mailing_answer_yes(message: Message, state: FSMContext):
    await state.set_state(Form.mailing_type)
    await message.answer(
        "Как ты хочешь получать расписание?",
        reply_markup=get_mailing_type()
    )

@router.message(F.text == "За некоторое время", Form.mailing_type)
async def mailing_type_before(message: Message, state: FSMContext):
    await state.update_data(mailing_type='before')
    await state.set_state(Form.mailing_time)
    await message.answer(
        "Укажи за сколько ты хочешь получать расписание:",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text == "В конкретное время", Form.mailing_type)
async def mailing_type_exact_time(message: Message, state: FSMContext):
    await state.update_data(mailing_type='exact_time')
    await state.set_state(Form.mailing_time)
    await message.answer(
        "Укажи во сколько ты хочешь получать расписание:",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text == "Я не хочу получать", Form.mailing_type)
async def mailing_cansel(message: Message, state: FSMContext):
    ...