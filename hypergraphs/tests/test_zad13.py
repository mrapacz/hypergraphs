from unittest import TestCase
from draw import Draw

class TestAproxPlot(TestCase):

    def test_aprox_plot_red(self):
        d = Draw(0,0,2,2)
        d.approx((255, 0, 0), (255, 0 , 0), (255, 0, 0), (255, 0, 0))
        result = d.get_approx()
        self.assertEqual(result[0],[[255.,255.,255.],[255.,255.,255.],[255.,255.,255.]])
        self.assertEqual(result[1],[[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])
        self.assertEqual(result[2],[[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])
        d.draw()


    def test_aprox_plot_green(self):
        d = Draw(0,0,2,2)
        d.approx((0, 255, 0), (0, 255 , 0), (0, 255, 0), (0, 255, 0))
        result = d.get_approx()
        self.assertEqual(result[0], [[0., 0., 0.], [0., 0., 0.], [0., 0., 0.]])
        self.assertEqual(result[1],[[255.,255.,255.],[255.,255.,255.],[255.,255.,255.]])
        self.assertEqual(result[2],[[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])
        d.draw()

    def test_aprox_plot_blue(self):
        d = Draw(0,0,2,2)
        d.approx((0, 0, 255), (0, 0 , 255), (0, 0, 255), (0, 0, 255))
        result = d.get_approx()
        self.assertEqual(result[0], [[0., 0., 0.], [0., 0., 0.], [0., 0., 0.]])
        self.assertEqual(result[1],[[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])
        self.assertEqual(result[2],[[255.,255.,255.],[255.,255.,255.],[255.,255.,255.]])
        d.draw()

    def test_aprox_plot_white(self):
        d = Draw(0,0,2,2)
        d.approx((255, 255, 255), (255, 255 , 255), (255, 255, 255), (255, 255, 255))
        result = d.get_approx()
        self.assertEqual(result[0],[[255.,255.,255.],[255.,255.,255.],[255.,255.,255.]])
        self.assertEqual(result[1],[[255.,255.,255.],[255.,255.,255.],[255.,255.,255.]])
        self.assertEqual(result[2],[[255.,255.,255.],[255.,255.,255.],[255.,255.,255.]])
        d.draw()

    def test_aprox_plot_black(self):
        d = Draw(0,0,2,2)
        d.approx((0, 0, 0), (0, 0 , 0), (0, 0, 0), (0, 0, 0))
        result = d.get_approx()
        self.assertEqual(result[0], [[0., 0., 0.], [0., 0., 0.], [0., 0., 0.]])
        self.assertEqual(result[1], [[0., 0., 0.], [0., 0., 0.], [0., 0., 0.]])
        self.assertEqual(result[2], [[0., 0., 0.], [0., 0., 0.], [0., 0., 0.]])
        d.draw()

    def test_aprox_plot_mystic(self):
        d = Draw(0,0,2,2)
        d.approx((219, 76, 119), (219, 76, 119), (219, 76, 119), (219, 76, 119))
        result = d.get_approx()
        self.assertEqual(result[0], [[219., 219., 219.], [219., 219., 219.], [219., 219., 219.]])
        self.assertEqual(result[1], [[76., 76., 76.], [76., 76., 76.], [76., 76., 76.]])
        self.assertEqual(result[2], [[119., 119., 119.], [119., 119., 119.], [119., 119., 119.]])
        d.draw()

    def test_abc(self):
        d = Draw(0, 0, 100, 100)
        d.approx((0, 255, 0), (0, 255, 0), (255, 0, 255), (255, 0, 255))
        d.draw()