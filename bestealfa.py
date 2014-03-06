# -*- coding: utf8 -*-

"""
   KARN voting app in Google App Engine
    Copyright (C) 2014 Klubb Alfa Romeo Norge <webmaster@klubbalfaromeo.no>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import cgi
import webapp2
import urllib
import jinja2
import os.path
import datetime

from google.appengine.ext import ndb
from google.appengine.api import users


JINJA_ENVIRONMENT=jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

VOTE_NAME = 'sedan_1978plus'
COOKIE_NAME = 'karn_vote_'+VOTE_NAME

def alt_key(id=VOTE_NAME):
    return ndb.Key('Alternative', id)

class Alternative(ndb.Model):
    """ Alternative entity """
    id = ndb.StringProperty()
    order = ndb.IntegerProperty()
    title = ndb.StringProperty()
    subtitle = ndb.StringProperty()
    image = ndb.StringProperty()
    description = ndb.StringProperty()

class Vote(ndb.Model):
    """ Vote entity """
    vote_id = ndb.StringProperty()
    ip_address = ndb.StringProperty()
    member_no = ndb.StringProperty()
    email = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        alt_query = Alternative.query(ancestor=alt_key()).order(Alternative.order)
        alternatives = alt_query.fetch(10)

        voted_cookie = self.request.cookies.get(COOKIE_NAME)
        already_voted = False
        if voted_cookie:
            already_voted = True

        template_data = {
            'alternatives': alternatives,
            'already_voted': already_voted,
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_data))


class VotePage(webapp2.RequestHandler):
    def post(self):
        vote = Vote(parent=alt_key())
        vote.vote_id = self.request.get('vote-id')
        vote.ip_address = self.request.remote_addr
        vote.member_no = self.request.get('memberno')
        vote.email = self.request.get('email')

        if not self.sane_values(vote.vote_id, vote.member_no, vote.email):
            self.redirect('/')
            return

        vote.put()
        # todo: add cookie
        much_much_later = datetime.datetime.now()+datetime.timedelta(days=365)
        self.response.set_cookie(COOKIE_NAME, 'voted', expires=much_much_later)
        self.redirect('/')

    def sane_values(self, vote, member_no, email):
        if not vote or len(vote) < 2:
            return False

        if not member_no or len(member_no) < 4:
            return False

        return True

class DataStoreInit(webapp2.RequestHandler):
    def get(self):
        # "Hmm" you might be thinking here :)
        alt_query = Alternative.query(ancestor=alt_key()).order(Alternative.order)
        alternatives = alt_query.fetch(10)
        if len(alternatives) == 0:
            self.put_alternative(1, 'alfetta', 'Alfa Romeo Alfetta', '1972-1987', u'<p><strong>Alfetta</strong> kom både som sedan og coupe - dette er sedanutgaven.</p><p>Sedanmodellen er designed av Centro Stile Alfa Romeo. Gearkassen og clutchen var plassert bak; dette er en såkalt <strong>transaksel</strong>.</p><p>Dette var en svært populær modell, ikke minst på grunn av lav vekt, gode kjøreegenskaper og en relativt kraftig motor etter datidens standard.</p><p>Det ble produsert over 400.000 Alfetta totalt.</p>')
            self.put_alternative(2, 'giulietta', 'Alfa Romeo Giulietta', '1977-1985', u'<p><strong>Giulietta Nuovo</strong> som denne også kalles siden det er det andre bilen fra Alfa Romeo som heter Giulietta.</p><p>Dette var en videreutivkling av Alfetta med en mer tidsriktig styling. Den fantes kun i sedanutgave.</p><p>I likhet med Alfetta var dette en <strong>transaksel</strong> med gearkassen montert bak.</p><p>Den absolutt raskeste utgaven av denne ble laget av <strong>Autodelta</strong> og het <strong>Giulietta Turbodelta</strong> med 170hk under panseret.</p>')
            self.put_alternative(3, 'alfa6', 'Alfa Romeo Alfa 6', '1979-1985', u'<p>Alfa 6 (eller <strong>Alfa Sei</strong> som den også kalles) var en virkelig direktørbil når den ble lansert i 1979.</p><p>I motsetning til andre samtidige Alfa så hadde den gearkassen og clutchen montert foran, antageligvis for å maksimere plassen i baksetet</p><p>Om man tittet under panseret kunne man se den første versjonen av den legendariske <strong>"busso"</strong> V6-motoren som ble brukt i forskjellige Alfa Romeo helt frem til 166 gikk ut av produksjon.</p>')
            self.put_alternative(4, '90', 'Alfa Romeo 90', '1984-1987', u'<p>Alfa 90 var lansert som en mellomting mellom Alfa 6 og Giulietta. Den hadde mange morsomme detaljer, blant annet kom det ned en spoiler i fremkant når en kom over en viss fart og man fikk en stresskoffert som passet perfekt inn i dashboardet.</p><p>Om man kjøpte toppmodelen QO - Quadrifoglio Oro - så fikk man digitale instrumenter, elektriske vinduer, tripcomputer og sentrallås.</p><p>over 56 000 biler ble solgt i løpet av fire år.</p>')
            self.put_alternative(5, '75', 'Alfa Romeo 75', '1985-1992', u'<p>Alfa 75 ble lansert som Giulietta Nuovo-erstatteren og fikk navnet for å feire at Alfa Romeo hadde 75-årsjubileum.</p><p>Utseendet er kileformet og svært karakteristisk - og kjøreegenskapene var i toppklasse; som på 90, Giulietta og Alfetta var dette en <strong>transaksel</strong> så vektfordelingen var det lite å utsette på.</p><p>Den hvasseste utgaven kom i 1987 og het <strong>Turbo Evoluzione</strong> og var en spesiell homogloberingsutgave. Effekten var oppgitt til å være 155hk.</p>')
            self.put_alternative(6, '164', 'Alfa Romeo 164', '1987-1998', u'<p>164 er den siste bilen Alfa Romeo konstruerte på egen hånd før firmaet ble kjøpt av Fiat.</p><p>Den ble konstruert på <strong>type 4</strong>-plattformen som var et samarbeid med Lancia, Fiat og Saab.</p><p>164 var også den siste bilen som ble solgt i Nord-Amerika før Alfa Romeo trakk seg ut og det ruller fortsatt en og annen 164 på amerikanske highways.</p><p>De to toppmodellene QV og Q4 hadde en V6 med 232hk - den samme motoren som i Alfa 6.</p>')
            self.put_alternative(7, '155', 'Alfa Romeo 155', '1992-1998', u'<p>155 var erstatteren til 75 og designet bærer en del likhetstrekk med 75 men det var en helt ny bil; nå med forhjulstrekk.</p><p>I 1995 ble det lansert en <strong>widebody</strong>-utgave av bilen med litt bredere sporvidde og bredere hjulbuer</p><p>Det ble også bygd en 155 Q4 TI for racing men den hadde ikke mye til felles med originalen; en V6 med 490hk på 11.900rpm (!) er i overkant mye for en gatebil men man kunne få kjøpt en Q4 Turbo med 190hk under panseret.</p>')
            self.put_alternative(8, '156', 'Alfa Romeo 156', '1996-2007', u'<p>156 var - som navnet antyder - etterfølgeren til 155 og var en stor suksess. Over 680.000 ble produsert fra 1997 til 2005.</p><p>Motoralternativene var mange - fra 1.6 liter og fire sylindre til 3.2 V6 ("busso"-motoren fra Alfa 6) pluss diesler fra 1.9 til 2.4 liter.</p><p>I 2001 kom <strong>GTA</strong> som hadde fått navn etter 60-tallets GTA. Den hadde bla. en V6 på 250hk, stivere hjuloppheng, større bremser og skinninteriør.</p>')
            self.put_alternative(9, '166', 'Alfa Romeo 166', '1996-2007', u'<p>Alfa 166 var erstatteren for 164 og siktet seg inn på direktørbil-segmentet. Den var fullpakket med utstyr og kom med motoralternativer fra 2 liter til 3.2 liter.</p><p>Utseendet var karakteristisk og det er lett å se en 166 i trafikken. I 2003 kom det en facelift med en annen grill og man kunne få en V6 på 3.2 liter.</p>')
            self.put_alternative(10, '159', 'Alfa Romeo 159', '2004-2011', u'<p>159 har fått navn etter den legendariske racerbilen <strong>159 Alfetta</strong>. I løpet av produksjonsperioden gjennomgikk den en rekke forandringer men utseendet (designet av Guigiaro) har stort sett vært likt fra start til slutt.</p><p>Det var en hel rekke motoralternativer - fra 1.8 bensin til 3.2 V6.</p><p>Toppmodellen hadde en 3.2-liters V6 og Q4 med 260hk. Motoren var produsert av Holden i Australia men fikk en liten tune-up i Italia før den ble montert.</p>')

        self.redirect('/')

    def put_alternative(self, order, id, title, subtitle, description):
        alt = Alternative(parent = alt_key())
        alt.order = order
        alt.id = id
        alt.title = title
        alt.subtitle = subtitle
        alt.image = 'images/' + id + '.jpg'
        alt.description = description
        alt.put()



application = webapp2.WSGIApplication([
        ('/', MainPage),
        ('/vote', VotePage),
        ('/init', DataStoreInit)
    ], debug=True)
