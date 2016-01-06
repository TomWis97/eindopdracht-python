import logging
logger = logging.getLogger('mainlogger')

def create_html(maincontent):
    """Krijgt de content van de pagina binnen en hangt er een header en footer omheen."""
    status = """Status: 200 OK
Content-Type: text/html

    """
    header = """<!DOCTYPE html>
<html>
	<head>
		<title>Dashboard</title>
		<link rel="stylesheet" type="text/css" href="style.css">
		<meta charset="utf-8">
        <style>
            @font-face: {
            	font-family: open-sans;
            	src: url('fonts/open-sans.ttf');
            }

            @font-face: {
            	font-family: roboto-bold;
            	src: url('fonts/roboto-bold.ttf');
            }

            @font-face: {
            	font-family: roboto-light;
            	src: url('fonts/roboto-light.ttf');
            }

            body {
            	background-image: url('bk.png');
            	width: 400px;
            	margin: auto;
            	font-family: open-sans, sans-serif;
            }

            header {
            	margin: 15px 0 2px 0;
            	border-radius: 10px 10px 0 0;
            	border: 1px solid #EEEEEE;
            	text-align: center;
            	background-image: url('bk2.png');
            	font-family: roboto-bold;
            }

            main {
            	background-image: url('bk1.png');
            	border-radius: 0  0 10px 10px;
                padding: 5px;
            }

            #online-stat {
            	height: 75px;
            	margin: auto;
            	padding: 10px;
            	display: block;
            }

            #overview {
            	width: 380px;
            	overflow: hidden;
            }
        </style>
	</head>
	<body>
		<header>
			<h1>Dashboard.</h1>
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
