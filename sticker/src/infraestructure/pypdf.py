from pathlib import Path

from fpdf import FPDF


class PyPdf(FPDF):
    line_heigth = 0.4
    align = "L"
    bold = " "
    br = 0

    row_height = None
    widths = []
    aligns = []
    bolds = []
    borders = []

    def __init__(self):
        self.my_pdf = FPDF.__init__(self, "P", "cm", "A4")

    def getMaxWidth(self) -> float:
        return float(self.w - self.r_margin - self.l_margin - (2 * self.c_margin))

    def getYPageEnd(self) -> float:
        y0 = int(self.page_break_trigger) - 1
        y1 = int(self.y) + 1
        return y0 if y1 < y0 else y1

    # adds a page break if h is too high
    def PageBreak(self, h) -> int:
        # If the height h would cause an overflow, add a new page immediately
        if (self.y + h) > self.page_break_trigger and self.accept_page_break():
            self.add_page(self.cur_orientation)
            return 1
        else:
            return 0

    def row(self, data: list, wds: list = []):
        # Calculate the height of the row
        nb = 0
        # width calculate
        l = len(data) if len(data) > 0 else 1
        lwds = len(wds)
        if l == lwds:
            self.widths = wds
        else:
            div = self._width() / l
            for i in range(l - lwds):
                self.widths.append(div)
        # calculate row and colums
        l_row_col = (1, 1)
        for i in range(l):
            if data[i] is not None:
                # nb = max(nb, self.NbLines(self.widths[i], data[i]))
                l_row_col = max(l_row_col, self.NbLines(self.widths[i], data[i]))
        nb = l_row_col[0] if l_row_col[0] > 0 else 1
        nc = l_row_col[1]

        h = self.ln_h * nb
        if self.row_square is not None and self.row_square > h:
            h = self.row_square

        # Issue a page break first if needed
        # Generate issue when nb take a page
        self.PageBreak(h)
        # Draw the cells of the row
        for i in range(len(data)):
            w = self.widths[i]

            try:
                a = self.aligns[i]
            except Exception:
                if self.align == "L":
                    a = "L"
                else:
                    a = self.align
            try:
                b = self.bolds[i]
            except Exception:
                if self.bold == " ":
                    b = " "
                else:
                    b = "B"
            try:
                br = self.borders[i]
            except Exception:
                if self.br == 0:
                    br = 0
                else:
                    br = 1

            # Save the current position
            x = self.get_x()
            y = self.get_y()

            # Draw the border
            if br == 1:
                self.rect(x, y, w, h)
            # font
            if b == "B":
                self.set_font("", "B")
            # Print the text
            try:
                texto = str(data[i])
            except Exception:
                texto = " "
            # Vertical align
            # print('------------TEST')
            # print(data[i])
            # print(nb)
            # print(nc)
            # texto=self.vertical_align(data[i], nb, nc)
            # print(texto)
            self.multi_cell(w, self.ln_h, texto, 0, a)

            self.set_font("")
            # Put the position to the right of the cell
            self.set_xy(x + w, y)

        # Go to the next line
        self.ln(h)
        # Reset
        self.bolds = []
        self.aligns = []
        self.borders = []
        self.row_square = None
