from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from datetime import datetime


class DatePickerPopup(Popup):
    day_spinner = ObjectProperty(None)
    month_spinner = ObjectProperty(None)
    year_spinner = ObjectProperty(None)

    def __init__(self, input_field, **kwargs):
        super(DatePickerPopup, self).__init__(**kwargs)
        self.title = 'Select Birth Date'
        self.size_hint = (None, None)
        self.size = (500, 250)
        self.auto_dismiss = False
        self.input_field = input_field

        layout = BoxLayout(orientation='vertical', spacing=10)

        self.day_spinner = Spinner(
            text=str(datetime.now().day),
            values=[str(day) for day in range(1, 32)],
            size_hint=(None, None),
            size=(80, 44),
        )

        self.month_spinner = Spinner(
            text=datetime.now().strftime('%B'),
            values=('January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'),
            size_hint=(None, None),
            size=(150, 44),
        )

        self.year_spinner = Spinner(
            text=str(datetime.now().year),
            values=[str(year) for year in range(1900, datetime.now().year + 1)],
            size_hint=(None, None),
            size=(100, 44),
        )

        layout.add_widget(self.day_spinner)
        layout.add_widget(self.month_spinner)
        layout.add_widget(self.year_spinner)

        button_layout = BoxLayout(spacing=10)
        ok_button = Button(text='OK', size_hint=(None, None), size=(100, 44))
        ok_button.bind(on_press=self.dismiss_popup)
        cancel_button = Button(text='Cancel', size_hint=(None, None), size=(100, 44))
        cancel_button.bind(on_press=self.dismiss)
        button_layout.add_widget(ok_button)
        button_layout.add_widget(cancel_button)

        layout.add_widget(button_layout)

        self.content = layout

    def dismiss_popup(self, instance):
        selected_day = int(self.day_spinner.text)
        selected_month = datetime.strptime(self.month_spinner.text, '%B').month
        selected_year = int(self.year_spinner.text)
        selected_date = datetime(selected_year, selected_month, selected_day)
        current_date = datetime.now()

        if selected_date <= current_date:
            self.birth_date = selected_date.strftime('%B %d, %Y')
            self.input_field.text = self.birth_date
            self.dismiss()
        else:
            self.dismiss()
            Popup(title="Invalid Date",
                  content=Label(text="Birth date cannot be in the future."),
                  size_hint=(None, None), size=(300, 150)).open()


class SelectionPopup(Popup):
    spinner = ObjectProperty(None)

    def __init__(self, options, input_field, defects_input, title, **kwargs):
        super(SelectionPopup, self).__init__(**kwargs)
        self.title = title
        self.size_hint = (None, None)
        self.size = (300, 400)
        self.auto_dismiss = False
        self.input_field = input_field
        self.defects_input = defects_input
        self.selected_items = set()

        layout = BoxLayout(orientation='vertical', spacing=10)

        for option in options:
            toggle_button = ToggleButton(text=option, size_hint=(None, None), size=(100, 44))
            toggle_button.bind(on_release=self.on_button_release)
            layout.add_widget(toggle_button)

        button_layout = BoxLayout(spacing=10)
        ok_button = Button(text='OK', size_hint=(None, None), size=(100, 44))
        ok_button.bind(on_press=self.dismiss_popup)
        cancel_button = Button(text='Cancel', size_hint=(None, None), size=(100, 44))
        cancel_button.bind(on_press=self.dismiss)
        button_layout.add_widget(ok_button)
        button_layout.add_widget(cancel_button)

        layout.add_widget(button_layout)

        self.content = layout

    def on_button_release(self, instance):
        if instance.state == 'down':
            self.selected_items.add(instance.text)
            self.update_defects_input(instance.text)
        else:
            self.selected_items.remove(instance.text)
            self.update_defects_input(instance.text, remove=True)

    def update_defects_input(self, model_name, remove=False):
        current_text = self.defects_input.text
        if remove:
            lines = current_text.split('\n')
            updated_text = '\n'.join(line for line in lines if model_name not in line)
        else:
            updated_text = f"{current_text}\nDefects for {model_name}:"
        self.defects_input.text = updated_text.strip()

    def dismiss_popup(self, instance):
        if self.selected_items:
            self.input_field.text = ', '.join(self.selected_items)
        else:
            self.input_field.text = "None selected"
        self.dismiss()


class GenderSelectionPopup(Popup):
    def __init__(self, input_field, **kwargs):
        super(GenderSelectionPopup, self).__init__(**kwargs)
        self.title = 'Select Gender'
        self.size_hint = (None, None)
        self.size = (200, 200)
        self.auto_dismiss = False
        self.input_field = input_field

        layout = BoxLayout(orientation='vertical', spacing=10)

        male_button = Button(text='Male', size_hint=(None, None), size=(100, 44))
        male_button.bind(on_press=self.select_gender)
        female_button = Button(text='Female', size_hint=(None, None), size=(100, 44))
        female_button.bind(on_press=self.select_gender)

        layout.add_widget(male_button)
        layout.add_widget(female_button)

        self.content = layout

    def select_gender(self, instance):
        self.input_field.text = instance.text
        self.dismiss()


class SurveyPage(GridLayout):
    def __init__(self, **kwargs):
        super(SurveyPage, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Name-surname:'))
        self.name_input = TextInput(multiline=False)
        self.name_input.bind(text=self.check_all_filled)
        self.add_widget(self.name_input)

        self.add_widget(Label(text='Birth Date:'))
        self.birth_date_input = Button(text='Select Date')
        self.birth_date_input.bind(on_press=self.show_date_picker)
        self.add_widget(self.birth_date_input)

        self.add_widget(Label(text='Education Level:'))
        self.education_input = TextInput(multiline=False)
        self.education_input.bind(text=self.check_all_filled)
        self.add_widget(self.education_input)

        self.add_widget(Label(text='City:'))
        self.city_input = TextInput(multiline=False)
        self.city_input.bind(text=self.check_all_filled)
        self.add_widget(self.city_input)

        self.add_widget(Label(text='Gender:'))
        self.gender_input = Button(text='Select Gender')
        self.gender_input.bind(on_press=self.show_gender_popup)
        self.add_widget(self.gender_input)

        self.add_widget(Label(text='AI model/type:'))
        self.ai_input = Button(text='Select AI Model')
        self.ai_input.bind(on_press=self.show_ai_popup)
        self.add_widget(self.ai_input)

        self.add_widget(Label(text='Defects or cons:'))
        self.defects_input = TextInput(multiline=True)
        self.defects_input.bind(text=self.check_all_filled)
        self.add_widget(self.defects_input)

        self.add_widget(Label(text='Beneficial use cases of AI:'))
        self.use_cases_input = TextInput(multiline=True)
        self.use_cases_input.bind(text=self.check_all_filled)
        self.add_widget(self.use_cases_input)

        self.send_button = Button(text='Send', background_color=(0.2, 0.2, 0.2, 1), disabled=True)
        self.send_button.bind(on_press=self.send_survey)
        self.add_widget(self.send_button)

    def show_date_picker(self, instance):
        popup = DatePickerPopup(self.birth_date_input)
        popup.open()

    def show_gender_popup(self, instance):
        popup = GenderSelectionPopup(self.gender_input)
        popup.open()

    def show_ai_popup(self, instance):
        options = ['ChatGPT', 'Bard', 'Claude', 'Copilot']
        popup = SelectionPopup(options, self.ai_input, self.defects_input, 'Select AI Model')
        popup.open()

    def check_all_filled(self, instance, value):
        # Check if all fields are filled, enable Send button if true
        if all([self.name_input.text, self.birth_date_input.text, self.education_input.text,
                self.city_input.text, self.gender_input.text, self.ai_input.text,
                self.defects_input.text, self.use_cases_input.text]):
            self.send_button.background_color = (0.2, 0.7, 0.3, 1)  # Change button color
            self.send_button.disabled = False  # Enable the "Send" button
        else:
            self.send_button.background_color = (0.2, 0.2, 0.2, 1)  # Change button color
            self.send_button.disabled = True  # Disable the "Send" button

    def send_survey(self, instance):
        # Check if all fields are filled
        if all([self.name_input.text, self.birth_date_input.text, self.education_input.text,
                self.city_input.text, self.gender_input.text, self.ai_input.text,
                self.defects_input.text, self.use_cases_input.text]):
            # Implement sending survey data here
            print("Survey Data Sent!")
        else:
            print("Please fill in all fields before sending the survey data.")


class SurveyApp(App):
    def build(self):
        return SurveyPage()


if __name__ == '__main__':
    SurveyApp().run()
