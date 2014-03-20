# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'pickupApp_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'pickupApp', ['Location'])

        # Adding model 'Sport'
        db.create_table(u'pickupApp_sport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'pickupApp', ['Sport'])

        # Adding model 'Game'
        db.create_table(u'pickupApp_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('dateCreated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('timeStart', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('cap', self.gf('django.db.models.fields.IntegerField')()),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='creator_of_game', to=orm['auth.User'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pickupApp.Location'])),
            ('sport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pickupApp.Sport'])),
        ))
        db.send_create_signal(u'pickupApp', ['Game'])

        # Adding M2M table for field users on 'Game'
        m2m_table_name = db.shorten_name(u'pickupApp_game_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('game', models.ForeignKey(orm[u'pickupApp.game'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['game_id', 'user_id'])

        # Adding model 'Comment'
        db.create_table(u'pickupApp_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('timeStamp', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pickupApp.Game'])),
            ('commenter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'pickupApp', ['Comment'])

        # Adding model 'InstagramInfo'
        db.create_table(u'pickupApp_instagraminfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('profile_picture', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('instagramID', self.gf('django.db.models.fields.IntegerField')()),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'pickupApp', ['InstagramInfo'])

        # Adding model 'GamePhoto'
        db.create_table(u'pickupApp_gamephoto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thumbnail', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('standard', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pickupApp.Game'])),
        ))
        db.send_create_signal(u'pickupApp', ['GamePhoto'])

        # Adding model 'UserInfo'
        db.create_table(u'pickupApp_userinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile_picture', self.gf('django.db.models.fields.URLField')(default='http://fashionlawsymposium.com/wp-content/uploads/2013/10/person-placeholder.jpg', max_length=200)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'pickupApp', ['UserInfo'])

        # Adding model 'UserSportLevel'
        db.create_table(u'pickupApp_usersportlevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('sport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pickupApp.Sport'])),
            ('level', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'pickupApp', ['UserSportLevel'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'pickupApp_location')

        # Deleting model 'Sport'
        db.delete_table(u'pickupApp_sport')

        # Deleting model 'Game'
        db.delete_table(u'pickupApp_game')

        # Removing M2M table for field users on 'Game'
        db.delete_table(db.shorten_name(u'pickupApp_game_users'))

        # Deleting model 'Comment'
        db.delete_table(u'pickupApp_comment')

        # Deleting model 'InstagramInfo'
        db.delete_table(u'pickupApp_instagraminfo')

        # Deleting model 'GamePhoto'
        db.delete_table(u'pickupApp_gamephoto')

        # Deleting model 'UserInfo'
        db.delete_table(u'pickupApp_userinfo')

        # Deleting model 'UserSportLevel'
        db.delete_table(u'pickupApp_usersportlevel')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pickupApp.comment': {
            'Meta': {'object_name': 'Comment'},
            'commenter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pickupApp.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'timeStamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'pickupApp.game': {
            'Meta': {'object_name': 'Game'},
            'cap': ('django.db.models.fields.IntegerField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creator_of_game'", 'to': u"orm['auth.User']"}),
            'dateCreated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pickupApp.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sport': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pickupApp.Sport']"}),
            'timeStart': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
        },
        u'pickupApp.gamephoto': {
            'Meta': {'object_name': 'GamePhoto'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pickupApp.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'standard': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'pickupApp.instagraminfo': {
            'Meta': {'object_name': 'InstagramInfo'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instagramID': ('django.db.models.fields.IntegerField', [], {}),
            'profile_picture': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'pickupApp.location': {
            'Meta': {'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'pickupApp.sport': {
            'Meta': {'object_name': 'Sport'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lovers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'through': u"orm['pickupApp.UserSportLevel']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'pickupApp.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'profile_picture': ('django.db.models.fields.URLField', [], {'default': "'http://fashionlawsymposium.com/wp-content/uploads/2013/10/person-placeholder.jpg'", 'max_length': '200'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'pickupApp.usersportlevel': {
            'Meta': {'object_name': 'UserSportLevel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sport': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pickupApp.Sport']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['pickupApp']