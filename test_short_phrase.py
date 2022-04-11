class TestShortPhase:
    def test_print_short_phrase(self):
        phrase = input('Set a phrase: ')
        assert len(phrase) < 15, 'This phrase is longer than 15 characters'
