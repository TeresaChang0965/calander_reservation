from shiny import App, render, ui, reactive
import datetime
import pandas as pd
import calendar
import shinyswatch

today_year = datetime.datetime.today().year
today_month = datetime.datetime.today().month

app_ui = ui.page_fluid(
    shinyswatch.theme.darkly(),
    ui.div(
        ui.h1(
            {"style":
                "font-color: black;"
                "font-size: 30px;"},
            '預約頁面')
    ),
    ui.div(
        ui.p(
            {"style":
                "font-color: black;"
                "font-size: 20px;"},
            '使用方法:'
        ),
        ui.p({"style":
                "font-color: black;"
                "font-size: 12px;"},
            '----搜尋: 查看目前預約情況'
        ),
        ui.p({"style":
                "font-color: black;"
                "font-size: 12px;"},
            '----預約: 顯示預約是否成功'
        )
    ),
    ui.row(
        ui.column(3,
            ui.input_select(
                id= "year", 
                label= "Year",
                choices= [str(year) for year in range(2023, 2030)],
                selected= str(today_year)
            )
        ),
        ui.column(3,
            ui.input_select(
                id= "month", 
                label= "Month",
                choices= [str(month) for month in range(1, 12)],
                selected= str(today_month)
            )   
        ),
        ui.column(3,
            ui.output_ui(
                id = "day",
                selected= '1'
            ),
        )
    ),
    ui.input_select(
        id= 'person',
        label= 'Person',
        choices= ['A', 'B']
    ),
    ui.input_action_button(
        id= 'search', 
        label= '搜尋',
    ),
    ui.input_action_button(
        id= 'add', 
        label= '預約',
    ),
    ui.div(
        {"style": 
            "font-color: black;"
            "background-color: #0072E3;"
            "font-size: 20px;"},
        ui.output_ui(
            id= 'current_data_name')
    ),
    ui.output_data_frame(
        id = 'original_calander',
    ),
    ui.div(
        {"style": 
            "font-color: black;"
            "background-color: #0072E3;"
            "font-size: 20px;"},
        ui.output_ui(
            id= 'reserved_data_name')
    ),
    ui.output_data_frame(
       id = 'reserve_calander',
    ),
    ui.div(
        ui.p(
            {"style":
                "font-color: black;"
                "font-size: 12px;"},
            '備註: 預約完後，需再按一次搜尋，即可看到更新後的月曆。'
        )
    )
)


def server(input, output, session):
    user_change = dict()

    @output
    @render.ui
    @reactive.event(input.search)
    def current_data_name():
        year_select = input.year()
        month_select = input.month()
        return f'查看{year_select}年{month_select}月'
    
    
    @output
    @render.ui
    @reactive.event(input.add)
    def reserved_data_name():
        year_select = input.year()
        month_select = input.month()
        return f'{year_select}年{month_select}月----預約成功 !'
    
    
    @output
    @render.data_frame
    @reactive.event(input.search)
    def original_calander():
        year_select = input.year()
        month_select = input.month()
        days_in_month = calendar.monthrange(int(year_select), int(month_select))[1]
        data = pd.DataFrame(
                        index= ['A', 'B'],
                        columns= ['Person'] + [str(number) for number in range(1, days_in_month + 1)]
                )
        data.at['A', 'Person'] = 'A'
        data.at['B', 'Person'] = 'B'

        for cell_key, value in user_change.items():
            year, month, day, person = cell_key
            if year == year_select and month == month_select:
                data.at[str(person), str(day)] = '√'

        return render.DataGrid(data)

    @output
    @render.data_frame
    @reactive.event(input.add)
    def reserve_calander():
        year_select = input.year()
        month_select = input.month()
        person_select = input.person()
        day_select = input.day()
        days_in_month = calendar.monthrange(int(year_select), int(month_select))[1]
        data = pd.DataFrame(
                        index= ['A', 'B'],
                        columns= ['Person'] + [str(number) for number in range(1, days_in_month + 1)]
                )
        data.at['A', 'Person'] = 'A'
        data.at['B', 'Person'] = 'B'

        user_change[(year_select, month_select, str(day_select), person_select)] = '√'
        for cell_key, value in user_change.items():
            year, month, day, person = cell_key
            if year == year_select and month == month_select:
                data.at[str(person), str(day)] = '√'
        return render.DataGrid(data)


    @output
    @render.ui
    def day():
        year_select = input.year()
        month_select = input.month()
        days_in_month = calendar.monthrange(int(year_select), int(month_select))[1]
        day_select = [day +1 for day in range(0, int(days_in_month))] 
        return ui.input_select(id = "day", label = "Day", choices = day_select)


app = App(app_ui, server)


# & "C:\Users\Teresa\AppData\Local\Microsoft\WindowsApps\python3.11.exe" -m shiny run --port 63799 --reload "c:\\Users\\Teresa\\Desktop\\html\\app.py"