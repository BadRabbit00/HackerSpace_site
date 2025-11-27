from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from events.models import Event
from news.models import News
from inventory.models import Item, Loan

class Command(BaseCommand):
    help = 'Creates default groups and permissions for HackerSpace staff'

    def handle(self, *args, **options):
        # 1. Event Managers
        event_group, created = Group.objects.get_or_create(name='Event Managers')
        event_ct = ContentType.objects.get_for_model(Event)
        event_perms = Permission.objects.filter(
            content_type=event_ct, 
            codename__in=['add_event', 'change_event', 'delete_event']
        )
        event_group.permissions.set(event_perms)
        self.stdout.write(self.style.SUCCESS(f'Updated group: Event Managers with {event_perms.count()} permissions'))

        # 2. News Editors
        news_group, created = Group.objects.get_or_create(name='News Editors')
        news_ct = ContentType.objects.get_for_model(News)
        news_perms = Permission.objects.filter(
            content_type=news_ct, 
            codename__in=['add_news', 'change_news', 'delete_news']
        )
        news_group.permissions.set(news_perms)
        self.stdout.write(self.style.SUCCESS(f'Updated group: News Editors with {news_perms.count()} permissions'))

        # 3. Inventory Managers
        inv_group, created = Group.objects.get_or_create(name='Inventory Managers')
        item_ct = ContentType.objects.get_for_model(Item)
        loan_ct = ContentType.objects.get_for_model(Loan)
        
        inv_perms = Permission.objects.filter(
            content_type__in=[item_ct, loan_ct],
            codename__in=[
                'add_item', 'change_item', 'delete_item',
                'add_loan', 'change_loan', 'delete_loan'
            ]
        )
        inv_group.permissions.set(inv_perms)
        self.stdout.write(self.style.SUCCESS(f'Updated group: Inventory Managers with {inv_perms.count()} permissions'))
