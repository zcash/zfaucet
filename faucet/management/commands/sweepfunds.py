from django.core.management.base import BaseCommand, CommandError
from pyZcash.rpc.ZDaemon import *

class Command(BaseCommand):
	help = 'Sweeps coinbase rewards into first zaddr'

	def handle(self, *args, **options):
		zd = ZDaemon()
		unified = zd.z_listaccounts()
		zd.sweep_coinbase(unified[0]['addresses'][0]['ua'])
