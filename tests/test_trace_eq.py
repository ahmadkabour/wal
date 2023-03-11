'''Test equivalence of trace loaders'''
import unittest
from itertools import combinations

from wal.core import Wal

# pylint: disable=C0103,C0115,C0116,E1101

class TraceEqTest():

    def setUp(self):
        #self.traces = []
        self.traces = map(lambda f: f'tests/traces/{f}', self.traces)

    def wal_eval(self, data):
        wal = Wal()
        wal.load(data[0])
        return wal.eval(data[1])

    def eval_eq(self, p):
        res = list(map(lambda t: self.wal_eval([t, p]), self.traces))

        for pair in combinations(res, 2):
            self.assertEqual(pair[0], pair[1])

    def test_trace_name(self):
        self.eval_eq('TRACE-NAME')

    def test_signals(self):
        self.eval_eq('SIGNALS')

    def test_max_index(self):
        self.eval_eq('MAX-INDEX')

    def test_scopes(self):
        self.eval_eq('SCOPES')

    def test_goto_end(self):
        self.eval_eq("(do (while (step) 0) INDEX)")

    def test_ts_list(self):
        self.eval_eq("(map (lambda [x] TS@x) (range MAX-INDEX))")

    def test_all_signal_values(self):
        self.eval_eq("(map (lambda [x] (map get SIGNALS)@x) (range MAX-INDEX))")


class CounterEqualTest(TraceEqTest, unittest.TestCase):
    '''Test counter traces for equality'''

    def setUp(self):
        self.traces = ['counter.vcd', 'counter.fst']
        super().setUp()

    def test_group_clk(self):
        self.eval_eq('(groups clk)')

    def test_rising_clocks(self):
        self.eval_eq('(find (&& (! tb.clk) tb.clk)')

    def test_overflow(self):
        self.eval_eq('(count tb.overflow')

    def test_local_scopes(self):
        self.eval_eq('LOCAL-SCOPES')
        self.eval_eq("(in-scope 'tb CS)")
        self.eval_eq("(in-scope 'tb LOCAL-SCOPES)")

    def test_local_signals(self):
        self.eval_eq("(in-scope 'tb LOCAL-SIGNALS)")
