import logging
logger = logging.getLogger('mainlogger')

def create_html(maincontent):
    """Krijgt de content van de pagina binnen als een string en hangt er een header en footer omheen."""
    logger.debug('create_html gaat een pagina bakken met deze input:' + maincontent)
    status = """Status: 200 OK
Content-Type: text/html

"""
    header = """<!DOCTYPE html>
<html>
	<head>
		<title>Dashboard</title>
		<link rel="stylesheet" type="text/css" href="web_style.css">
		<meta charset="utf-8">
	</head>
	<body>
		<header>
			<h1>MonTool.</h1>
            <a href="web_dashboard.py">Dashboard</a><a href="web_add_device.py">Apparaat toevoegen.</a>
		</header>
		<main>"""

    footer = """</main>
		<footer>
			<p>Mick en Tom</p>
		</footer>
	</body>
</html>"""
    # We kunnen dit heel moeilijk doen, of heel makkelijk. Hier ben ik voor optie 2 gegaan.
    return status + header + maincontent + footer
