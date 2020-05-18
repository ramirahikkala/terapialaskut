# -*- coding: utf-8 -*-
'''
Handles PDF form filling
'''

from collections import OrderedDict
from PyPDF2 import PdfFileWriter, PdfFileReader


def _getFields(obj, tree=None, retval=None, fileobj=None):
    """
    Extracts field data if this PDF contains interactive form fields.
    The *tree* and *retval* parameters are for recursive use.

    :param fileobj: A file object (usually a text file) to write
        a report to on all interactive form fields found.
    :return: A dictionary where each key is a field name, and each
        value is a :class:`Field<PyPDF2.generic.Field>` object. By
        default, the mapping name is used for keys.
    :rtype: dict, or ``None`` if form data could not be located.
    """
    fieldAttributes = {
        '/FT': 'Field Type',
        '/Parent': 'Parent',
        '/T': 'Field Name',
        '/TU': 'Alternate Field Name',
        '/TM': 'Mapping Name',
        '/Ff': 'Field Flags',
        '/V': 'Value',
        '/DV': 'Default Value',
    }
    if retval is None:
        retval = OrderedDict()
        catalog = obj.trailer["/Root"]
        # get the AcroForm tree
        if "/AcroForm" in catalog:
            tree = catalog["/AcroForm"]
        else:
            return None
    if tree is None:
        return retval

    obj._checkKids(tree, retval, fileobj)
    for attr in fieldAttributes:
        if attr in tree:
            # Tree is a field
            obj._buildField(tree, retval, fileobj, fieldAttributes)
            break

    if "/Fields" in tree:
        fields = tree["/Fields"]
        for f in fields:
            field = f.getObject()
            obj._buildField(field, retval, fileobj, fieldAttributes)

    return retval


def get_form_fields(infile):
    '''Returns fields of the document'''
    infile = PdfFileReader(open(infile, 'rb'))
    fields = _getFields(infile)
    return OrderedDict((k, v.get('/V', '')) for k, v in fields.items())


def update_form_values(infile, outfile, newvals=None):
    '''Fill values and create new PDF file'''
    pdf = PdfFileReader(open(infile, 'rb'))
    writer = PdfFileWriter()

    for i in range(pdf.getNumPages()):
        page = pdf.getPage(i)

        if newvals:
            writer.updatePageFormFieldValues(page, newvals)
        else:
            writer.updatePageFormFieldValues(
                page,
                {k: f'#{i} {k}={v}' for i, (k, v) in enumerate(get_form_fields(infile).items())},
            )

        writer.addPage(page)

    with open(outfile, 'wb') as out:
        writer.write(out)


def prepare_directory_structure(filename):
    import datetime
    import pathlib

    current = datetime.datetime.now()

    report_path = (
        pathlib.Path.cwd()
        / 'kela_lomakkeet'
        / str(current.year)
        / str(current.month)
    )
    report_path.mkdir(parents=True, exist_ok=True)

    report_file_path = report_path / (filename + '.pdf')

    return report_file_path


def write_invoice(therapist, customer):

    file_name = prepare_directory_structure(customer.name)

    fields = {
        'tx02': customer.name,
        'tx03': customer.id_number,
        'tx03': customer.id_number,
        'tx04': therapist.company_name,
        'tx05': therapist.id_number,
        'tx06': therapist.phone_number,
        'tx07': therapist.email,
        'tx08': therapist.iban,
        'tx09': therapist.bic,
        'tx80': therapist.name,
    }

    import datetime

    fields['tx119'] = datetime.date.today().strftime("%d.%m.%Y")

    index = 0

    with open(str(file_name).replace('.pdf', '.txt'), 'w') as out_file:
        out_file.write(customer.name + "\n\n")
        out_file.write("Tuntihinta: " + str(customer.hour_price) + "\n\n")
        out_file.write("Sähköposti: " + customer.email + "\n\n")
        out_file.write("Osoite: " + customer.street_address + "\n\n")
        out_file.write("Kelakorvaus: " + str(therapist.kelakorvaus) + "\n\n")
        out_file.write("Laskutustapa: " + customer.way_of_billing + "\n\n")

        out_file.write("Käynnit:\n")
        total_cost = 0
        total_without_kela = 0

        for visit in sorted(customer.visits, key=lambda x: x.visit_date):
            fields['tx' + str(16 + index * 3)] = visit.visit_date.strftime("%d.%m.%Y")
            fields['tx' + str(17 + index * 3)] = visit.visit_type
            fields['tx' + str(18 + index * 3)] = visit.cost
            index += 1
            total_cost += visit.cost
            total_without_kela += visit.cost - therapist.kelakorvaus
            out_file.write(str(index) + ": " + visit.visit_date.strftime("%d.%m.%Y") + "\n")

        out_file.write("\n")
        out_file.write("Yht: " + str(total_cost))
        out_file.write("\nOmavastuu " + str(total_without_kela))


    update_form_values('pdf_originals/ku205.pdf', file_name, fields)


def write_tilitys(therapist, customers, reference_number=None, biller=None, invoicer=None):
    '''
    biller = tilityksen laatija
    invoicer = Kuntoutuspalveluntuottajan ilmoittama laskuttajan nimi
    '''

    file_name = prepare_directory_structure('tilitys')

    fields = {
        'tx04': therapist.company_name,
        'tx05': therapist.id_number,  # y-tunnus or henkilötunnus
        'tx06': therapist.street_address,
        'tx07': therapist.phone_number,
        'tx13': therapist.iban,
        'tx14': therapist.bic,
        'tx120': therapist.name,
    }

    if reference_number:
        fields['tx16'] = reference_number

    if invoicer:
        fields['tx08'] = invoicer.name
        fields['tx09'] = invoicer.id_number

    if biller:
        fields['tx10'] = biller.name
        fields['tx11'] = biller.phone_number
        fields['tx12'] = biller.fax

    nro = 0

    for customer in customers:
        fields['tx' + str(19 + nro * 5)] = str(nro + 1)
        fields['tx' + str(20 + nro * 5)] = customer.name
        fields['tx' + str(21 + nro * 5)] = customer.id_number
        fields['tx' + str(22 + nro * 5)] = customer.unbilled_time()
        fields['tx' + str(23 + nro * 5)] = customer.unbilled_total()

        nro += 1

    fields['tx121'] = sum([cust.unbilled_total() for cust in customers])

    fields['tx03'] = len(customers)

    import datetime

    fields['tx119'] = datetime.date.today().strftime("%d.%m.%Y")

    update_form_values('pdf_originals/ku206.pdf', file_name, fields)


if __name__ == '__main__':
    from pprint import pprint

    pdf_file_name = 'ku205.pdf'

    pprint(get_form_fields('pdf_originals/' + pdf_file_name))

    update_form_values(
        'pdf_originals/' + pdf_file_name, 'out-' + pdf_file_name
    )  # enumerate & fill the fields with their own names
    update_form_values(
        'pdf_originals/' + pdf_file_name,
        'out2-' + pdf_file_name,
        {'tx04': 'Psykologipalvelu Riikka Rahikkala', 'tx05': 'My Another'},
    )  # update the form fields
