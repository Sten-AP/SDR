#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Oefening 4
# Author: sten
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



class Labo_8(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Oefening 4", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Oefening 4")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "Labo_8")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.select = select = True
        self.samp_rate = samp_rate = 100
        self.afstand = afstand = 0

        ##################################################
        # Blocks
        ##################################################

        _select_check_box = Qt.QCheckBox("'select'")
        self._select_choices = {True: 1, False: 0}
        self._select_choices_inv = dict((v,k) for k,v in self._select_choices.items())
        self._select_callback = lambda i: Qt.QMetaObject.invokeMethod(_select_check_box, "setChecked", Qt.Q_ARG("bool", self._select_choices_inv[i]))
        self._select_callback(self.select)
        _select_check_box.stateChanged.connect(lambda i: self.set_select(self._select_choices[bool(i)]))
        self.top_layout.addWidget(_select_check_box)
        self.network_tcp_source_0 = network.tcp_source.tcp_source(itemsize=gr.sizeof_char*1,addr='127.0.0.1',port=12345,server=False)
        self.network_tcp_sink_0 = network.tcp_sink(gr.sizeof_float, 1, '127.0.0.1', 12444,2)
        self.digital_psk_mod_0 = digital.psk.psk_mod(
            constellation_points=16,
            mod_code="gray",
            differential=True,
            samples_per_symbol=8,
            excess_bw=0.35,
            verbose=False,
            log=False)
        self.digital_psk_demod_0 = digital.psk.psk_demod(
            constellation_points=16,
            differential=True,
            samples_per_symbol=8,
            excess_bw=0.35,
            phase_bw=(6.28/100.0),
            timing_bw=(6.28/100.0),
            mod_code="gray",
            verbose=False,
            log=False)
        self.blocks_vector_source_x_0 = blocks.vector_source_b((65, 66, 67, 10), True, 1, [])
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(3, gr.GR_MSB_FIRST)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_selector_0 = blocks.selector(gr.sizeof_char*1,select,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, 8)
        self._afstand_range = Range(0, 2, 0.01, 0, 200)
        self._afstand_win = RangeWidget(self._afstand_range, self.set_afstand, "'afstand'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._afstand_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_delay_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.digital_psk_mod_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.network_tcp_sink_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.digital_psk_demod_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.digital_psk_mod_0, 0), (self.digital_psk_demod_0, 0))
        self.connect((self.network_tcp_source_0, 0), (self.blocks_selector_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Labo_8")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_select(self):
        return self.select

    def set_select(self, select):
        self.select = select
        self._select_callback(self.select)
        self.blocks_selector_0.set_input_index(self.select)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_afstand(self):
        return self.afstand

    def set_afstand(self, afstand):
        self.afstand = afstand




def main(top_block_cls=Labo_8, options=None):

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
