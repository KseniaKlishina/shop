# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'id')),
                ('title', models.CharField(unique=True, max_length=50, db_column=b'title')),
                ('name', models.CharField(max_length=256, db_column=b'name', db_index=True)),
                ('description', models.TextField(db_column=b'description', blank=True)),
            ],
            options={
                'db_table': 'category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'id')),
                ('category_id', models.ForeignKey(to='website.Category', db_column=b'category_id')),
            ],
            options={
                'db_table': 'category_image',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'id')),
                ('name', models.CharField(max_length=20, db_column=b'name')),
            ],
            options={
                'db_table': 'city',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'id')),
                ('name', models.CharField(unique=True, max_length=20, db_column=b'name')),
            ],
            options={
                'db_table': 'country',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'id')),
                ('city_id', models.ForeignKey(to='website.City', db_column=b'city_id')),
            ],
            options={
                'db_table': 'delivery',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'id')),
                ('title', models.CharField(max_length=50, db_column=b'title')),
                ('price', models.IntegerField(db_column=b'price')),
                ('type', models.PositiveIntegerField(db_column=b'type')),
                ('rating', models.SmallIntegerField(db_column=b'rating')),
                ('description', models.TextField(db_column=b'description', blank=True)),
            ],
            options={
                'db_table': 'goods',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GoodsCategories',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'id')),
                ('category_id', models.ForeignKey(to='website.Category', db_column=b'category_id')),
                ('goods_id', models.ForeignKey(to='website.Goods', db_column=b'goods_id')),
            ],
            options={
                'db_table': 'goods_categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'id')),
                ('url', models.CharField(unique=True, max_length=256, db_column=b'url')),
            ],
            options={
                'db_table': 'image',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'id')),
                ('title', models.CharField(unique=True, max_length=50, db_column=b'title')),
                ('description', models.TextField(db_column=b'description', blank=True)),
                ('email', models.EmailField(max_length=20, db_column=b'email', blank=True)),
                ('telephone', models.CharField(max_length=20, db_column=b'telephone', blank=True)),
                ('address', models.CharField(max_length=256, db_column=b'address', blank=True)),
                ('city_id', models.ForeignKey(to='website.City', db_column=b'city_id')),
                ('logo_id', models.ForeignKey(db_column=b'logo_id', blank=True, to='website.Image', null=True)),
            ],
            options={
                'db_table': 'organization',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='goodscategories',
            unique_together=set([('goods_id', 'category_id')]),
        ),
        migrations.AddField(
            model_name='goods',
            name='organization_id',
            field=models.ForeignKey(to='website.Organization', db_column=b'organization_id'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goods',
            name='picture_id',
            field=models.ForeignKey(db_column=b'picture_id', to='website.Image', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='goods',
            unique_together=set([('title', 'organization_id')]),
        ),
        migrations.AddField(
            model_name='delivery',
            name='goods_id',
            field=models.ForeignKey(to='website.Goods', db_column=b'goods_id'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='delivery',
            unique_together=set([('goods_id', 'city_id')]),
        ),
        migrations.AddField(
            model_name='city',
            name='country_id',
            field=models.ForeignKey(to='website.Country', db_column=b'country_id'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('country_id', 'name')]),
        ),
        migrations.AddField(
            model_name='categoryimage',
            name='image_id',
            field=models.ForeignKey(to='website.Image', db_column=b'image_id'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='categoryimage',
            unique_together=set([('category_id', 'image_id')]),
        ),
    ]
