# -*- coding: utf-8 -*-
"""
Created on: 2015.01.11.

Author: turbo

Classes for storing settings and filters, applicable for any Storm or Confocal file loaded.
"""

from functools import partial

from .filters import *
import copy

"""functions starting with 'apply' in child Settings classes
are called upon pressing the correspondent Apply button
"""
class Settings(object):
    def __init__(self, *args, **kwargs):
        pass

    def _setup_components(self, main_window, type_):
        widgets = list(main_window.__dict__.keys())
        self.push_buttons = [getattr(main_window, obj_name) for obj_name in widgets if obj_name.find('pushButton') != -1 and obj_name.find(type_) != -1]
        self.radio_buttons = [getattr(main_window, obj_name) for obj_name in widgets if obj_name.find('radioButton') != -1 and obj_name.find(type_) != -1]
        self.check_boxes = [getattr(main_window, obj_name) for obj_name in widgets if obj_name.find('checkBox') != -1 and obj_name.find(type_) != -1]
        self.combo_boxes = [getattr(main_window, obj_name) for obj_name in widgets if obj_name.find('comboBox') != -1 and obj_name.find(type_) != -1]
        self.spin_boxes = [getattr(main_window, obj_name) for obj_name in widgets if (obj_name.find('spinBox') != -1 or obj_name.find('doubleSpinBox') != -1) and obj_name.find(type_) != -1]
        self.group_boxes = [getattr(main_window, obj_name) for obj_name in widgets if obj_name.find('groupBox') != -1 and obj_name.find(type_) != -1]

    def _add_input_handlers(self):
        for push_button in self.push_buttons:
            push_button.clicked.connect(partial(self._on_setting_changed, push_button))
        for radio_button in self.radio_buttons:
            radio_button.toggled.connect(partial(self._on_setting_changed, radio_button))
        for check_box in self.check_boxes:
            check_box.stateChanged.connect(partial(self._on_setting_changed, check_box))
        for combo_box in self.combo_boxes:
            combo_box.currentIndexChanged.connect(partial(self._on_setting_changed, combo_box))
        for spin_box in self.spin_boxes:
            spin_box.valueChanged.connect(partial(self._on_setting_changed, spin_box))
        for group_box in self.group_boxes:
            group_box.toggled.connect(partial(self._on_setting_changed, group_box))

    def _init_settings_values(self):
        all_setting_widgets = self.push_buttons + self.radio_buttons + self.check_boxes \
                              + self.combo_boxes + self.spin_boxes + self.group_boxes
        for setting_widget in all_setting_widgets:
            self._on_setting_changed(setting_widget, is_init=True)

    def setup(self, main_window, type_):
        self.main_window = main_window
        self._setup_components(main_window, type_)
        self._init_settings_values()
        self._add_input_handlers()

    def _on_setting_changed(self, setting_widget, is_init=False):
        setting_widget_qt_type = type(setting_widget).__name__
        setting_key = '_'.join(str(setting_widget.objectName()).split('_')[1:])
        # TODO: refactor, cleanup logic and conventions here
        if setting_widget_qt_type == 'QGroupBox':
            # if this groupbox is a filter, enable/disable the filter
            if setting_key.find('filter') != -1:
                for filter_ in self.filters:
                    if filter_.name_prefix == setting_key:
                        filter_.enabled = setting_widget.isChecked()
        elif setting_widget_qt_type == 'QRadioButton':
            setattr(self, setting_key, setting_widget.isChecked())
        elif setting_widget_qt_type == 'QCheckBox':
            setattr(self, setting_key, setting_widget.isChecked())
        elif setting_widget_qt_type == 'QComboBox':
            setattr(self, setting_key, setting_widget.currentText())
        elif setting_widget_qt_type == 'QSpinBox' or setting_widget_qt_type == 'QDoubleSpinBox':
            setattr(self, setting_key, setting_widget.value())
        elif setting_widget_qt_type == 'QPushButton':
            # if an applyer button
            if str(setting_widget.objectName()).find('apply') != -1:
                if not is_init:
                    try:
                        func = getattr(self, setting_key)
                        func()
                    except AttributeError:
                        print("no method to run with this apply button's naming convention")


class StormSettings(Settings):
    def __init__(self, *args, **kwargs):
        super(StormSettings, self).__init__(*args, **kwargs)
        self.roi_counter = 0
        self.rois = []
        self.filters = []
        self.filters.append(ZFilter('storm_filter_z'))
        self.filters.append(PhotonFilter('storm_filter_photon'))
        self.filters.append(FrameFilter('storm_filter_frame'))
        self.filters.append(LocalDensityFilter('storm_filter_localdensity'))

    def get_roi_counter(self):
        self.roi_counter += 1
        return self.roi_counter

    def set_rois(self):
        self.rois = self.main_window.viewer.current_storm_image.roi_list

    def setup_filters(self):
        for filter_ in self.filters:
            filter_.setup(self)

    def filter_storm_data(self, points=None):
        filtered_points = copy.deepcopy(points)
        for filter_ in self.filters:
            if filter_.enabled:
                filtered_points = filter_.run(filtered_points)
        return filtered_points

    def add_roi(self, roi):
        self.rois.append(roi)
        self.main_window.tabWidget_storm_tabs.setCurrentIndex(3)
        self.main_window.storm_roi_list.addItem(roi)
        self.main_window.storm_roi_list.setCurrentRow(self.main_window.storm_roi_list.count()-1)

    def clear_rois(self):
        for i in range(len(self.rois)):
            self.remove_roi(0)

    def remove_roi(self, index):
        removed = self.main_window.storm_roi_list.takeItem(index)
        if removed:
            self.main_window.storm_roi_list.setCurrentRow(-1)
            self.rois.pop(index)
            return removed
        else:
            return False

    def set_default_values(self):
        self.set_storm_config()

    def set_storm_config(self, image=None):
        if image:
            image.coords_cols = (
                self.main_window.storm_settings.storm_config_fileheader_x,
                self.main_window.storm_settings.storm_config_fileheader_y,
                self.main_window.storm_settings.storm_config_fileheader_z
            )
            image.other_cols = (
                self.main_window.storm_settings.storm_config_fileheader_localization_precision,
                self.main_window.storm_settings.storm_config_fileheader_channel_name,
                self.main_window.storm_settings.storm_config_fileheader_photon,
                self.main_window.storm_settings.storm_config_fileheader_frame
            )
            self.main_window.viewer.display.storm_dot_size = self.main_window.storm_settings.storm_config_dot_size

    def apply_storm_filters(self):
        imgs = self.main_window.storm_images_list.selectedItems()
        if imgs:
            self.main_window.viewer.show_storm_image(imgs)
        else:
            self.main_window.show_error(message='No STORM file is opened!')

    def apply_storm_config(self):
        imgs = self.main_window.storm_images_list.selectedItems()
        if imgs:
            for image in imgs:
                self.set_storm_config(image)
                image.isParsingNeeded = True
            self.main_window.viewer.show_storm_image(imgs)
        else:
            self.main_window.show_error(message='No STORM file is opened!')



class ConfocalSettings(Settings):
    def __init__(self, *args, **kwargs):
        super(ConfocalSettings, self).__init__(*args, **kwargs)


    def set_default_values(self):
        self.set_confocal_config()
        self.set_confocal_display()

    def set_confocal_config(self):
        resampling_min = ''
        resampling_mag = ''
        for radio_button in self.radio_buttons:
            obj_name = str(radio_button.objectName())
            if radio_button.isChecked() and obj_name.find('confocal_config') != -1:
                if "min" in obj_name:
                    resampling_min = obj_name.split('_')[-1]
                if "mag" in obj_name:
                    resampling_mag = obj_name.split('_')[-1]
        self.main_window.viewer.display.QWindow.set_sim_interpolation(resampling_min, resampling_mag)

    def set_confocal_display(self):
        self.main_window.viewer.display.ConfocalTransparency = self.confocal_display_appear_transparency
        self.main_window.viewer.display.ConfocalZNum = self.confocal_display_appear_zposition-1
        try:
            px = self.main_window.viewer.display.ConfocalMetaData['SizeX']
        except KeyError:
            px = self.confocal_config_calibration_px
        #self.main_window.viewer.display.Viewbox.ConfocalOffset = [
        #    self.confocal_display_offset_y / (100 * px),
        #    self.confocal_display_offset_x / (100 * px)
        #]


    def apply_confocal_config(self):
        imageList = self.main_window.confocal_images_list.selectedItems()
        self.set_confocal_config()
        if imageList:
            #fertigstellen
            imageList[0].isParsingNeeded = True
            self.main_window.viewer.show_confocal_image(imageList, ApplyButton=True)
        else:
            self.main_window.show_error(message='No Confocal file is opened!')

    def apply_confocal_display(self):
        imageList = self.main_window.confocal_images_list.selectedItems()
        self.set_confocal_display()
        if imageList:
            imageList[0].isParsingNeeded = False
            self.main_window.viewer.show_confocal_image(imageList, ApplyButton=True)
        else:
            self.main_window.show_error(message='No Confocal file is opened!')


