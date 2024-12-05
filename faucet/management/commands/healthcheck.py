from django.core.management.base import BaseCommand
from faucet.models import HealthCheck
from pyZcash.rpc.ZDaemon import ZDaemon


class Command(BaseCommand):
    help = 'Updates blockchain health values shown on the main page'

    def handle(self, *args, **options):
        self.stdout.write('Updating blockchain health values...')

        try:
            zd = ZDaemon()

            # Fetch balance details
            balance = zd.z_gettotalbalance()
            if not balance:
                raise ValueError("z_gettotalbalance returned an empty response.")

            t_balance = balance.get('transparent', 0)
            z_balance = balance.get('private', 0)

            # Fetch network stats
            height = zd.getNetworkHeight()
            difficulty = zd.getNetworkDifficulty()

            # Save health check data
            hc = HealthCheck()
            hc.t_balance = t_balance
            hc.z_balance = z_balance
            hc.height = height
            hc.difficulty = difficulty
            hc.save()

            self.stdout.write('Blockchain health values updated successfully.')

        except Exception as e:
            self.stderr.write(f"Error updating blockchain health values: {e}")
