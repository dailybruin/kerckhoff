import math
from django.utils.functional import cached_property
from django.core.paginator import Page

class Paginator:
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
        self.object_list = object_list
        self.per_page = int(per_page)
        self.orphans = int(orphans)
        self.allow_empty_first_page = allow_empty_first_page

    def validate_number(self, number): # make sure number is an int
        """Validate the given 1-based page number."""
        if number < 1:
            raise Exception('That page number is less than 1')
        if number > self.num_pages:
            if not (number == 1 and self.allow_empty_first_page):
                raise Exception('That page contains no results')
        return number

    def get_page(self, number):
        """Return a Page object for the given 1-based page number."""
        try:
            number = self.validate_number(number)
        except Exception:
            number = self.num_pages
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return Page(self.object_list[bottom:top], number, self)

    @cached_property
    def count(self):
        """Return the total number of objects, across all pages."""
        return len(self.object_list)

    @cached_property
    def num_pages(self):
        """Return the total number of pages."""
        if self.count == 0 and not self.allow_empty_first_page:
            return 0
        hits = max(1, self.count - self.orphans)
        return math.ceil(hits / self.per_page)

    
