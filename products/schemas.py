import orjson
from bson import ObjectId
from pydantic import BaseModel, Field

from configs import get_configs


class ObjID(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class ProductSchema(BaseModel):
    id: ObjID | None = Field(alias='_id')
    title: str = Field(description='Название')
    brand: str
    category: str
    description: str | None
    descr_from_excel: str | None
    recommend_price: str | None
    recommend_price_with_symbol: str | None = Field(description='Рекомендованная цена')
    photo_url: str | None
    photo_urls: list | None
    images: list | None
    telegram_file_ids: list | None
    rated_power: str | None = Field(description='Номинальная мощность, кВт')
    weight_netto: str | None = Field(description='Вес (нетто), кг')
    working_volume: str | None = Field(description='Рабочий объём, см3')
    max_rpm: str | None = Field(description='Максимальное количество оборотов/мин')
    type_engine: str | None = Field(description='Тип двигателя')
    engine_oil_volume: str | None = Field(description='Объем масла в двигателе, л')
    launch: str | None = Field(description='Запуск')
    cylinder_diameter: str | None = Field(description='Диаметр цилиндра, мм')
    piston_stroke: str | None = Field(description='Ход поршня, мм')
    fuel_tank_capacity: str | None = Field(description='Емкость топливного бака, л')
    lighting_coil: str | None = Field(description='Катушка освещения')
    the_presence_of_a_gearbox: str | None = Field(description='Наличие редуктора')
    shaft_location: str | None = Field(description='Расположение вала')
    fuel_supply_system: str | None = Field(description='Система подачи топлива')
    engine_model: str | None = Field(description='Модель двигателя')
    torque: str | None = Field(description='Крутящий момент')
    shaft_diameter: str | None = Field(description='Диаметр вала, мм')
    compression_ratio: str | None = Field(description='Степень сжатия')
    engine: str | None = Field(description='Двигатель')
    engine_displacement: str | None = Field(description='Рабочий объем двигателя, см3')
    pipe_diameter: str | None = Field(description='Диаметр трубы')
    launch_system: str | None = Field(description='Система запуска')
    lifting_height: str | None = Field(description='Высота подъема, м')
    performance: str | None = Field(description='Производительность')
    fence_depth: str | None = Field(description='Глубина забора, м')
    power: str | None = Field(description='Мощность, кВт')
    dimensions: str | None = Field(description='Габаритные размеры')
    oil_tank_volume: str | None = Field(description='Объем масляного бака, л')
    gasoline_diesel: str | None = Field(description='Бензин/Дизель')
    fuel_tank_volume: str | None = Field(description='Объем топливного бака, л')
    water_quality: str | None = Field(description='Качество воды')
    weight_brutto: str | None = Field(description='Вес(брутто), кг')
    fraction_size: str | None = Field(description='Размер фракции')
    max_power: str | None = Field(description='Макс. мощность, л.с.')
    vendor_code: str | None = Field(description='Артикул')
    manufacturer: str | None
    preparation_for_work: str | None = Field(description='Подготовка к работе, сек')
    manufacturers_warranty: str | None = Field(description='Гарантия производителя, мес')
    description: str | None = Field(description='Описание товара')
    recommend_price_with_symbol: str | None  # = Field(description='Рекомендованная цена')
    ats: str | None = Field(alias='ATS', description='ATS (автоматический ввод резерва)')
    applied_engine_power: str | None = Field(description='Мощность применяемого двигателя')
    alternator: str | None = Field(description='Альтернатор')
    degree_of_protection: str | None = Field(description='Степень защиты')
    output_voltage: str | None = Field(description='Выходное напряжение')
    output_frequency: str | None = Field(description='Выходная частота')
    noise_level: str | None = Field(description='Уровень шума, дБ')
    availability_of_outlets: str | None = Field(description='Наличие розеток')
    number_of_phases: str | None = Field(description='Количество фаз')
    availability_of_batteries: str | None = Field(description='Наличие АКБ')
    availability_of_wheels: str | None = Field(description='Наличие колес')
    availability_of_handles: str | None = Field(description='Наличие ручек')
    rated_current: str | None = Field(description='Номинальный ток, А')
    packing_dimensions: str | None = Field(description='Размеры упаковки, мм')
    automatic_voltage_regulator: str | None = Field(description='AVR (автоматический регулятор напряжения)')
    alternator_winding: str | None = Field(description='Обмотка альтернатора')
    generator_type: str | None = Field(description='Тип генератора')
    rated_generator_power: str | None = Field(description='Номинальная мощность генератора, КВт')
    fuel_consumption_g: str | None = Field(description='Расход топлива, г/кВт*ч')
    fuel_consumption_lc: str | None = Field(description='Расход топлива, л/ ч')
    time_of_continuous_work: str | None = Field(description='Время непрерывной работы, часов')
    idle_speed: str | None = Field(description='Обороты холостого хода, об/мин')
    shaft_length: str | None = Field(description='Длина вала, мм')
    engine_type: str | None = Field(description='Тип двигателя')
    shaft_type: str | None = Field(description='Тип вала')
    presence_of_a_gearbox: str | None = Field(description='Наличие редуктора')
    shaft_drawing: str | None = Field(description='Чертеж вала')
    engine_drawing: str | None = Field(description='Чертеж двигателя')
    ignition_system: str | None = Field(description='Система зажигания')
    fuel_consumption: str | None = Field(description='Расход топлива, г/кВт*ч')
    package_size: str | None = Field(description='Размеры упаковки, мм')
    minimum_retail_price: float | None
    wholesale_price: float | None
    availability: bool | None

    class Config:
        json_dumps = orjson.dumps
        json_loads = orjson.loads


class ProductResponseSchema(BaseModel):
    count_documents: int | None
    results: list[ProductSchema]


class Brand(BaseModel):
    id: int = Field(alias='_id')
    name: str


class Category(BaseModel):
    id: int = Field(alias='_id')
    name: str
    brand: str


class YandexS3StorageOptionsSchema(BaseModel):
    service_name: str = 's3'
    aws_access_key_id: str = get_configs().aws_access_key_id
    aws_secret_access_key: str = get_configs().aws_secret_access_key
    region_name: str = 'ru-central1'
    endpoint_url: str = 'https://storage.yandexcloud.net'


class S3SBucketKeySchema(BaseModel):
    Bucket: str
    Key: str


class ServiceCenterSchema(BaseModel):
    id: ObjID | None = Field(alias='_id')
    name: str
    url: str | None
    phone: str | None
    region: str | None
    address: str | None
    latitude: str | None
    longitude: str | None

    @classmethod
    def from_id_to_object_id(cls, data: dict):
        _id = data.pop('id')
        return cls(_id=ObjectId(_id), **data).dict(by_alias=False)
