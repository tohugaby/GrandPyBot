from project.parser.parsers import LegacyParser, StopWordsParser, FrenchWordsParser, NonLettersParser, CitiesParser, \
    CountriesParser


class TestLegacyParser:
    def setup_method(self):
        self.in_string = "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?"

    def teardown_method(self):
        pass

    def test_parse_string(self):
        parser = LegacyParser(self.in_string)
        assert isinstance(parser.out_list, list)
        assert parser.out_list == self.in_string.split(" ")
        assert "d'OpenClassrooms" in parser.out_list


class TestNonLettersParser:
    def setup_method(self):
        self.in_string = "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?"

    def teardown_method(self):
        pass

    def test_parse_string(self):
        parser = NonLettersParser(self.in_string)
        assert isinstance(parser.out_list, list)
        assert parser.out_list != self.in_string
        assert len(self.in_string) > len(parser.out_list)
        assert "OpenClassrooms" in parser.out_list


class TestStopWordsParser:
    def setup_method(self):
        self.in_string = "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?"

    def teardown_method(self):
        pass

    def test_parse_string(self):
        parser = StopWordsParser(self.in_string)
        assert isinstance(parser.out_list, list)
        assert parser.out_list != self.in_string
        assert len(self.in_string) > len(parser.out_list)
        assert "OpenClassrooms" in parser.out_list


class TestFrenchWordsParser:
    def setup_method(self):
        self.in_string = "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?"

    def teardown_method(self):
        pass

    def test_parse_string(self):
        parser = FrenchWordsParser(self.in_string)
        assert isinstance(parser.out_list, list)
        assert parser.out_list != self.in_string
        assert len(self.in_string) > len(parser.out_list)
        assert "OpenClassrooms" in parser.out_list


class TestCitiesParser:
    def setup_method(self):
        self.in_string = "Bonjour vieille branche  ! Que peux-tu me dire sur Budapest ?"

    def teardown_method(self):
        pass

    def test_parse_string(self):
        parser = CitiesParser(self.in_string)
        assert isinstance(parser.out_list, list)
        assert parser.out_list != self.in_string
        assert len(self.in_string) > len(parser.out_list)
        assert "Budapest" in parser.out_list


class TestCountriesParser:
    def setup_method(self):
        self.in_string = "Ola  ! Que sais-tu du Japon ?"

    def teardown_method(self):
        pass

    def test_parse_string(self):
        parser = CountriesParser(self.in_string)
        assert isinstance(parser.out_list, list)
        assert parser.out_list != self.in_string
        assert len(self.in_string) > len(parser.out_list)
        assert "Japon" in parser.out_list

# class TestLastWordParser:
#     pass