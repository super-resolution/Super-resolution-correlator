# -*- coding: utf-8 -*-
"""
Created on: 2015.01.26.

Author: turbo


"""

from functools import partial

class RunnableComponent(object):
    def __init__(self, *args, **kwargs):
        self.name_prefix = args[0]
        self.enabled = False

    def _setup_components(self, all_config):
        # TODO: atfedo prefixek miatt itt tul sokat kaphat, pontos egyezest vizsgalni, ne indexOf-ot
        self.radio_buttons = [widget for widget in all_config.radio_buttons if str(widget.objectName()).find(self.name_prefix) != -1]
        self.check_boxes = [widget for widget in all_config.check_boxes if str(widget.objectName()).find(self.name_prefix) != -1]
        self.combo_boxes = [widget for widget in all_config.combo_boxes if str(widget.objectName()).find(self.name_prefix) != -1]
        self.spin_boxes = [widget for widget in all_config.spin_boxes if str(widget.objectName()).find(self.name_prefix) != -1]

    def _init_config_values(self):
        all_setting_widgets = self.radio_buttons + self.check_boxes + self.combo_boxes + self.spin_boxes
        for setting_widget in all_setting_widgets:
            self._on_setting_changed(setting_widget, is_init=True)

    def _add_input_handlers(self):
        for radio_button in self.radio_buttons:
            radio_button.toggled.connect(partial(self._on_setting_changed, radio_button))
        for check_box in self.check_boxes:
            check_box.stateChanged.connect(partial(self._on_setting_changed, check_box))
        for combo_box in self.combo_boxes:
            combo_box.currentIndexChanged.connect(partial(self._on_setting_changed, combo_box))
        for spin_box in self.spin_boxes:
            spin_box.valueChanged.connect(partial(self._on_setting_changed, spin_box))

    def setup(self, all_config):
        self._setup_components(all_config)
        self._init_config_values()
        self._add_input_handlers()

    def _on_setting_changed(self, setting_widget, is_init=False):
        setting_widget_qt_type = type(setting_widget).__name__
        setting_key = '_'.join(str(setting_widget.objectName()).split('_')[1:])
        if setting_widget_qt_type == 'QRadioButton':
            setattr(self, setting_key, setting_widget.isChecked())
        elif setting_widget_qt_type == 'QCheckBox':
            setattr(self, setting_key, setting_widget.isChecked())
        elif setting_widget_qt_type == 'QComboBox':
            setattr(self, setting_key, setting_widget.currentText())
        elif setting_widget_qt_type == 'QSpinBox' or setting_widget_qt_type == 'QDoubleSpinBox':
            setattr(self, setting_key, setting_widget.value())

    def run(self):
        pass
