import sys

## -------------------------
## Une ligne de programme
## -------------------------
class ligne(object):
	def __init__(self, nol, texte):
		self.nol = nol				## No ligne
		self.texte = texte			## Texte / instruction
		self.err = 0				## Erreur
		self.etiq = False			## Etiq Oui/non

## --------------
## Un programme
## --------------
class prog(object):
	## Codes Erreur
	ERR_DEB_FIN  = 100
	ERR_ETIQ_DUP = 101
	ERR_INSTR_INEX  = 102

	def __init__(self, nom):
		self.name = nom
		self.lignes = []
		self.cpt_lig = 0
		self.err = 0

		self.etiq = []

	def add_l(self, texte):
		self.cpt_lig += 1
		l = ligne( self.cpt_lig, texte)
		self.lignes.append(l)

	def check(self):
		## Debut / Fin
		if self.lignes[0].texte != "BEGIN":
			self.lignes[0].err = prog.ERR_DEB_FIN
			self.err += 1
		if self.lignes[-1].texte != "END":
			self.lignes[-1].err = prog.ERR_DEB_FIN
			self.err += 1

		## Verif Etiquette dupliquee
		for l in self.lignes:
			if l.texte.startswith('$'):
				if l.texte in self.etiq:
					l.err = prog.ERR_ETIQ_DUP
					self.err += 1
				else:
					self.etiq.append((l.texte, l.nol))
					l.etiq = True

		## Verif des instructions
		for l in self.lignes:
			if l.etiq:
				continue
			else:
				print( "L= %s " % l.texte )
				I = l.texte.split(" ")
				if I[0] in ( "BEGIN", "END", "READ", "PRINT" ):
					pass
				elif I[0] in ( "RESET", "JMP_FALSE", "JUMP_TRUE", "TEST", "GOTO" ):
					## Commande avec 1 parametres
					pass
				elif I[0] in ( "CALL", "FUNC" ):
					## Commande appel de lib externe
					pass
				elif I[0] in ( "SET" ):
					## Commande avec 2 parametres
					pass
				else:
					l.err = prog.ERR_INSTR_INEX

	def pr(self):
		print( "PROGRAMME : %s " % self.name )
		for l in self.lignes:
			if l.err:
				e = '*'
			else:
				e = ' '
			print( "%03d :%s: %s " % ( l.nol, e,  l.texte ) )
		print( "Erreur(s) : %s " % self.err )
		print( "Etiquette : %s " % self.etiq)

	def __str__(self):
		return "%s : %s " % (self.name, self.cpt_lig)

## -----------------
## Lecture du source
## -----------------
def lire(fichier):
	prg = prog( "TEST1" )
	f = open(fichier)
	for l in f.readlines():
		l = l.strip()
		if l.startswith('#'):
			continue
		elif len(l) == 0:
			continue
		else:
			w = l.split()
			prg.add_l(' '.join(w))
	return prg
			
## -----
## MAIN
## -----
if __name__ == '__main__':
	p = lire(sys.argv[1])
	print( p )
	p.check()
	p.pr()

