from unittest import TestCase

from mysql.connector.errors import Error

from .errors import handle_error, ERRORS, ERRORS_DICT


class ErrorsTestCase(TestCase):

    def test_errors(self):
        for errno, kofp_exc in ERRORS.items():
            error = Error(
                msg="BADmsg",
                errno=errno,
                sqlstate="BADsqlstate",
            )
            with self.assertRaises(kofp_exc) as exc:
                handle_error("bad", error)

            self.assertEqual(errno, exc.exception.args[0]['errno'])
            self.assertEqual("bad", exc.exception.args[0]['msg'])
            self.assertEqual("BADsqlstate", exc.exception.args[0]['sqlstate'])
            self.assertEqual(ERRORS_DICT["errno"], exc.exception.args[0]['errcode'])
