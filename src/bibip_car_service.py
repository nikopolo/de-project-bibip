from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from pathlib import Path
from decimal import Decimal
from datetime import datetime, date


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        with open(self.root_directory_path + "sales_index.txt", 'w') as ind:
                pass

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        with open(self.root_directory_path + "models.txt", 'a+') as f:
            str_for_add = f"{model.id}, {model.name}, {model.brand}".ljust(500)
            f.write(str_for_add)
            f.write('\n')

        # create index file if not exist
        if not Path(self.root_directory_path + "models_index.txt").is_file():
            with open(self.root_directory_path + "models_index.txt", 'w') as ind:
                pass

        with open(self.root_directory_path + "models_index.txt", 'r+') as ind:
            count_models = len(ind.readlines())
            ind.write(f'{count_models + 1}, {model.id}')
            ind.write('\n')
        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        with open(self.root_directory_path + "cars.txt", 'a+') as f:
            str_for_add = f'{car.vin}, {car.model}, {car.price}, {car.date_start.date()}, {car.status}'.ljust(500)
            f.write(str_for_add)
            f.write('\n')

        # create index file if not exist
        if not Path(self.root_directory_path + "cars_index.txt").is_file():
            with open(self.root_directory_path + "cars_index.txt", 'w') as ind:
                pass

        with open(self.root_directory_path + "cars_index.txt", 'r+') as ind:
            count_models = len(ind.readlines())
            ind.write(f'{count_models + 1}, {car.vin}'.ljust(500))
            ind.write('\n')
        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        model_car = 0
        search_sale_vin = sale.index()
        with open(self.root_directory_path + "cars_index.txt", 'r') as f:
            for i in f.readlines():
                if i.split(', ')[1].strip() == search_sale_vin:
                    model_car = int(i.split(', ')[0].strip())

        with open(self.root_directory_path + "cars.txt", 'r') as f:
            f.seek((model_car - 1) * (501))
            sell_car_list = f.read(500).strip().split(', ')

        with open(self.root_directory_path + "cars.txt", 'r+') as f:
            f.seek((model_car - 1) * (501))
            str_for_sold = f"{sell_car_list[0].strip()}, {sell_car_list[1]}, {sell_car_list[2]}, {sell_car_list[3]}, {CarStatus.sold}".strip().ljust(500)
            if model_car == 1 or model_car == 2:
                f.write(f'{str_for_sold}')
            else:
                f.write(f'\n{str_for_sold}')

        with open(self.root_directory_path + "sales.txt", 'a+') as f:
            str_for_add = f'{sale.sales_number}, {sale.car_vin}, {sale.sales_date}, {sale.cost}'.ljust(500)
            f.write(str_for_add)
            f.write('\n')

        # create index file if not exist
        if not Path(self.root_directory_path + "sales_index.txt").is_file():
            with open(self.root_directory_path + "sales_index.txt", 'w') as ind:
                pass
        with open(self.root_directory_path + "sales_index.txt", 'r+') as ind:
            count_models = len(ind.readlines())
            ind.write(f'{count_models + 1}, {sale.car_vin}'.ljust(500))
            ind.write('\n')
        return Car(vin=sale.car_vin, model=model_car, price=sale.cost, date_start=sale.sales_date, status=CarStatus.sold)

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        list_car = []
        with open(self.root_directory_path + "cars.txt", 'r') as f:
            for i in f.readlines():
                if str(i.split(', ')[4]).strip() == str(status):
                    list_car.append(Car(vin=i.split(', ')[0], model=int(i.split(', ')[1]), price=Decimal(i.split(', ')[2]), date_start=datetime.strptime(str(i.split(', ')[3]), "%Y-%m-%d"), status=CarStatus.available))
        return list_car

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        car_ind = 0
        with open(self.root_directory_path + "cars_index.txt", 'r') as f:
            for i in f.readlines():
                car_vin = i.split(', ')[1].strip()
                if car_vin == vin:
                    car_ind = int(i.split(', ')[0])
                    print(f'car_ind {car_ind}')
                    break
        if car_ind == 0:
            return None

        with open(self.root_directory_path + "cars.txt", 'r') as f:
            f.seek((car_ind - 1) * (501))
            find_car = f.read(500).strip().split(', ')
            find_model = int(find_car[1])

        with open(self.root_directory_path + "models.txt", 'r') as f:
            f.seek((find_model - 1) * (501))
            model_list = f.read(500).strip().split(', ')
            m_name = model_list[1]
            m_brand = model_list[2]

        with open(self.root_directory_path + "sales_index.txt", 'r') as f:
            is_car_sale = False
            for i in f.readlines():
                if i.split(', ')[1].strip() == car_vin:
                    sales_ind = i.split(', ')[0]
                    is_car_sale = True
                else:
                    is_car_sale = False

        if is_car_sale:
            with open(self.root_directory_path + "sales.txt", 'r') as f:
                f.seek((int(sales_ind) - 1) * (501))
                sale_car_list = f.read(500).strip().split(', ')
                sale_car_date = datetime.strptime(sale_car_list[2], "%Y-%m-%d %H:%M:%S")
                sale_car_cost = Decimal(sale_car_list[3])
        else:
            sale_car_date = None
            sale_car_cost = None

        car_full_info = CarFullInfo(
            vin=find_car[0],
            car_model_name=m_name,
            car_model_brand=m_brand,
            price=Decimal(str(find_car[2])),
            date_start=datetime.strptime(str(find_car[3]), "%Y-%m-%d"),
            status=CarStatus(find_car[4]),
            sales_date=sale_car_date,
            sales_cost=sale_car_cost
        )
        return car_full_info

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        '''Поиск и замена vin в cars_index'''
        with open(self.root_directory_path + "cars_index.txt", 'r') as f:
            for i in f.readlines():
                car_vin = i.split(', ')[1].strip()
                if car_vin == vin:
                    car_ind_vin = int(i.split(', ')[0])
                    break

        with open(self.root_directory_path + "cars_index.txt", 'r+') as f:
            f.seek((car_ind_vin - 1) * (501))
            new_index_car = f'{car_ind_vin}, {new_vin}'.ljust(500)
            if car_ind_vin == 1 or car_ind_vin == 2:
                f.write(f'{new_index_car}')
            else:
                f.write(f'\n{new_index_car}')

        '''Поиск и замена vin в cars'''
        with open(self.root_directory_path + "cars.txt", 'r') as f:
            f.seek((car_ind_vin - 1) * (501))
            car = f.read(500).strip().split(', ')

        with open(self.root_directory_path + "cars.txt", 'r+') as f:
            f.seek((car_ind_vin - 1) * (501))
            c_model = int(car[1])
            c_price = Decimal(car[2])
            c_date = datetime.strptime(car[3], "%Y-%m-%d")
            c_status = CarStatus(car[4])
            vin_change = f"{new_vin}, {car[1]}, {car[2]}, {car[3]}, {car[4]}".ljust(500)
            if car_ind_vin == 1 or car_ind_vin == 2:
                f.write(f'{vin_change}')
            else:
                f.write(f'\n{vin_change}')

        return Car(
            vin = new_vin,
            model = c_model,
            price = c_price,
            date_start = c_date,
            status = c_status
        )

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        '''Чтение данных sales в list, кроме заданного'''
        with open(self.root_directory_path + "sales.txt", 'r') as f:
            new_sales = []
            vin_for_del = ''
            for i in f.readlines():
                num_sale = i.strip().split(', ')[0]
                if num_sale == sales_number:
                    vin_for_del = i.strip().split(', ')[1]
                    print(f'vin_for_del {vin_for_del}.')
                    continue
                else:
                    new_sales.append(i.strip())
        print(f'vin_for_del {vin_for_del}.')

        '''Перезапись данных sales без переданного номера продажи'''
        with open(self.root_directory_path + "sales.txt", 'w') as f:
            for i in new_sales:
                f.write(i.ljust(500))
                f.write('\n')

        '''Чтение данных sales_index в list, кроме заданного'''
        with open(self.root_directory_path + "sales_index.txt", 'r') as f:
            new_sales_index = []
            print(f'index vin_for_del {vin_for_del}.')
            for i in f.readlines():
                if vin_for_del == i.strip().split(', ')[1]:
                    continue
                else:
                    new_sales_index.append(i.strip())

        with open(self.root_directory_path + "sales_index.txt", 'w') as f:
            for i in new_sales_index:
                f.write(i.ljust(500))
                f.write('\n')

        ''''''
        with open(self.root_directory_path + "cars_index.txt", 'r') as f:
            search_ind = ''
            for i in f.readlines():
                car_index_vin = i.strip().split(', ')[1]
                if vin_for_del == car_index_vin:
                    search_ind = i.strip().split(', ')[0]
                    break

        '''Поиск машины'''
        with open(self.root_directory_path + "cars.txt", 'r') as f:
            f.seek((int(search_ind) - 1) * (501))
            repair_car_list = f.read(500).strip().split(', ')


        with open(self.root_directory_path + "cars.txt", 'r+') as f:
            f.seek((int(search_ind) - 1) * (501))
            str_for_repair = f"{repair_car_list[0]}, {repair_car_list[1]}, {repair_car_list[2]}, {repair_car_list[3]}, available".ljust(500)
            f.write(str_for_repair)

        return Car(
            vin=repair_car_list[0],
            model=int(repair_car_list[1]),
            price=Decimal(repair_car_list[2],),
            date_start=datetime.strptime(repair_car_list[3], "%Y-%m-%d"),
            status=CarStatus(repair_car_list[4])
            )

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        sales_dict = {}
        '''Получаем список vin проданных машин'''
        sales_vin = []
        price_model_dell = []
        cars_id = []
        with open(self.root_directory_path + "sales.txt", 'r') as f:
            for i in f.readlines():
                sales_vin.append(i.strip().split(', ')[1])
                price_model_dell.append([i.strip().split(', ')[1], i.strip().split(', ')[3]])

        '''Получаем по vin машины'''
        with open(self.root_directory_path + "cars_index.txt", 'r') as f:
            for c_index in f.readlines():
                if c_index.strip().split(', ')[1] in sales_vin:
                    cars_id.append(c_index.strip().split(', ')[0])

        '''Находим список самых продаваемых'''
        temp_models_id = []
        with open(self.root_directory_path + "cars.txt", 'r') as f:
            for car_id in cars_id:
                f.seek((int(car_id) - 1) * (501))
                car_info = f.read(500).strip().split(', ')
                temp_models_id.append([car_info[0], car_info[1]])
                if car_info[1] not in sales_dict:
                    sales_dict[car_info[1]] = 1
                else:
                    sales_dict[car_info[1]] += 1
        sort_dict = sorted(sales_dict.items(), key=lambda item: item[1], reverse=True)


        all_sum_sales = {}
        for i in price_model_dell:
            for j in temp_models_id:
                if i[0] == j[0]:
                    if j[1] not in all_sum_sales:
                        all_sum_sales[j[1]] = float(i[1])
                    else:
                        all_sum_sales[j[1]] += float(i[1])

        for i in range(len(sort_dict)):
            if (i) == len(sort_dict) - 1:
                break
            if sort_dict[i][1] == sort_dict[i + 1][1] and all_sum_sales[sort_dict[i][0]] < all_sum_sales[sort_dict[i + 1][0]]:
                temp_var = sort_dict[i]
                sort_dict[i] = sort_dict[i+1]
                sort_dict[i+1] = temp_var


        '''Находим модели'''
        list_model_sale = []
        count_model = 0
        with open(self.root_directory_path + "models.txt", 'r') as f:
            for s_model in sort_dict:
                f.seek((int(s_model[0]) - 1) * (501))
                model = f.read(500).strip().split(', ')
                m_car_model = model[1]
                m_brand = model[2]
                list_model_sale.append(ModelSaleStats(
                    car_model_name=m_car_model,
                    brand=m_brand,
                    sales_number=s_model[1]
                ))
                count_model += 1
                if count_model == 3:
                    break
        return list_model_sale
