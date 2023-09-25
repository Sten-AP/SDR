#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import osmosdr
import time



from gnuradio import qtgui

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48e3
        self.ptt = ptt = 0
        self.intpol = intpol = 125
        self.decpol = decpol = 6
        self.PMR = PMR = 446006250
        self.AFgain = AFgain = 10

        ##################################################
        # Blocks
        ##################################################
        _ptt_push_button = Qt.QPushButton('')
        _ptt_push_button = Qt.QPushButton('ptt')
        self._ptt_choices = {'Pressed': 1, 'Released': 0}
        _ptt_push_button.pressed.connect(lambda: self.set_ptt(self._ptt_choices['Pressed']))
        _ptt_push_button.released.connect(lambda: self.set_ptt(self._ptt_choices['Released']))
        self.top_layout.addWidget(_ptt_push_button)
        # Create the options list
        self._PMR_options = [446006250, 446018750, 446031250, 446043750, 446056250, 446068750, 446081250, 446093750]
        # Create the labels list
        self._PMR_labels = map(str, self._PMR_options)
        # Create the combo box
        self._PMR_tool_bar = Qt.QToolBar(self)
        self._PMR_tool_bar.addWidget(Qt.QLabel("'PMR'" + ": "))
        self._PMR_combo_box = Qt.QComboBox()
        self._PMR_tool_bar.addWidget(self._PMR_combo_box)
        for _label in self._PMR_labels: self._PMR_combo_box.addItem(_label)
        self._PMR_callback = lambda i: Qt.QMetaObject.invokeMethod(self._PMR_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._PMR_options.index(i)))
        self._PMR_callback(self.PMR)
        self._PMR_combo_box.currentIndexChanged.connect(
            lambda i: self.set_PMR(self._PMR_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._PMR_tool_bar)
        self._AFgain_range = Range(0, 50, 1, 10, 200)
        self._AFgain_win = RangeWidget(self._AFgain_range, self.set_AFgain, "'AFgain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._AFgain_win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=intpol,
                decimation=decpol,
                taps=[],
                fractional_bw=0)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.pttsw = blocks.multiply_const_cc(ptt)
        self.osmosdr_sink_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_sink_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0.set_sample_rate(samp_rate*intpol/decpol)
        self.osmosdr_sink_0.set_center_freq(PMR+((1-ptt)*(-13500000)), 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(30, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(AFgain)
        self.audio_source_0 = audio.source(48000, '', False)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(0.5)
        self.analog_fm_preemph_0 = analog.fm_preemph(fs=samp_rate, tau=50e-6, fh=-1.0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_preemph_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.pttsw, 0))
        self.connect((self.audio_source_0, 0), (self.analog_fm_preemph_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.pttsw, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.pttsw, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.osmosdr_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate*self.intpol/self.decpol)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_ptt(self):
        return self.ptt

    def set_ptt(self, ptt):
        self.ptt = ptt
        self.osmosdr_sink_0.set_center_freq(self.PMR+((1-self.ptt)*(-13500000)), 0)
        self.pttsw.set_k(self.ptt)

    def get_intpol(self):
        return self.intpol

    def set_intpol(self, intpol):
        self.intpol = intpol
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate*self.intpol/self.decpol)

    def get_decpol(self):
        return self.decpol

    def set_decpol(self, decpol):
        self.decpol = decpol
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate*self.intpol/self.decpol)

    def get_PMR(self):
        return self.PMR

    def set_PMR(self, PMR):
        self.PMR = PMR
        self._PMR_callback(self.PMR)
        self.osmosdr_sink_0.set_center_freq(self.PMR+((1-self.ptt)*(-13500000)), 0)

    def get_AFgain(self):
        return self.AFgain

    def set_AFgain(self, AFgain):
        self.AFgain = AFgain
        self.blocks_multiply_const_vxx_0.set_k(self.AFgain)




def main(top_block_cls=top_block, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
