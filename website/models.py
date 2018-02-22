from django.db import models
from django.contrib.auth.models import User
# Contains every country in database
class Country(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=20, unique=True, blank=False, db_column='name')

    class Meta:
        db_table = 'country'

# Contains cities related with countries
class City(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    country_id = models.ForeignKey(Country, blank=False, db_column='country_id')
    name = models.CharField(max_length=20, blank=False, db_column='name')

    class Meta:
        db_table = 'city'
        unique_together=('country_id', 'name')

# Contains links to images
# All images ARE publicaly availible from Internet
class Image(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    url = models.CharField(max_length=256, blank=False, unique=True, db_column='url')

    class Meta:
        db_table = 'image'

# Contains information about organzation (wich provides concrete Goods&Services)
class Organization(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')

    # General information
    title = models.CharField(max_length=50, blank=False, unique=True, db_column='title')
    logo_id = models.ForeignKey(Image, null=True, blank=True, db_column='logo_id')
    description = models.TextField(blank=True, db_column='description')
    
    # Contacts
    email = models.EmailField(max_length=20, blank=True, db_column='email')
    telephone = models.CharField(max_length=20, blank=True, db_column='telephone')
    city_id = models.ForeignKey(City, blank=False, db_column='city_id')
    address = models.CharField(max_length=256, blank=True, db_column='address');
   
    
    class Meta:
        db_table = 'organization'

# Describes a single goods category
class Category(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    title = models.CharField(max_length=50, blank=False, unique=True, db_column='title')
    name = models.CharField(max_length=256, blank=False, db_index=True, db_column='name')
    description = models.TextField(blank=True, db_column='description')

    class Meta:
        db_table = 'category'

# Explicitly defines ManyToMany tables relation: Many images for a many categories 
class CategoryImage(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    category_id = models.ForeignKey(Category, blank=False, db_column='category_id')
    image_id = models.ForeignKey(Image, blank=False, db_column='image_id')

    class Meta:
        db_table = 'category_image'
        unique_together = ('category_id', 'image_id')



class Advertising(models.Model):
     id = models.AutoField(primary_key=True, db_column='id')
     image_id = models.ForeignKey(Image, blank=False, db_column='image_id')
     description = models.TextField(blank=True, db_column='description')
     
     class Meta:
        db_table = 'Advertising'
        unique_together = ('id', 'image_id')

        
 
class Events (models.Model):
     id = models.AutoField(primary_key=True, db_column='id')
     title = models.CharField(max_length=100, blank=False, db_column='title')
     description=models.TextField(blank=True, db_column='description')
     contents=models.TextField(blank=True, db_column='contents')
     image_id = models.ForeignKey(Image, blank=False, db_column='image_id')
     pub_date = models.DateTimeField('date published')

     
     class Meta:
        db_table = 'events'
        unique_together = ('id', 'image_id')
    
    

# Explicitly defines ManyToMany tables relation for: 

# Describes Goods&Services wich are sold in the store
class Goods(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    title = models.CharField(max_length=50, blank=False, db_column='title')
    price = models.IntegerField(blank=False, db_column='price')
    # For future use: will contain unique property (use django choises in future)
    type = models.PositiveIntegerField(blank=False, db_column='type')
    organization_id = models.ForeignKey(Organization, blank=False, db_column='organization_id')
    rating = models.SmallIntegerField(blank=False, db_column='rating')
    picture_id = models.ForeignKey(Image, null=True, blank=False, db_column='picture_id')
    description = models.TextField(blank=True,  db_column='description')
    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        db_table = 'goods'
        unique_together = ('title', 'organization_id')

# Decription of region where the goods can be delivered
class Delivery(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    goods_id = models.ForeignKey(Goods, blank=False, db_column='goods_id')
    city_id = models.ForeignKey(City, blank=False, db_column='city_id')

    class Meta:
        db_table = 'delivery'
        unique_together = ('goods_id', 'city_id')

# Explicitly binds goods and their categories
class GoodsCategories(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    goods_id = models.ForeignKey(Goods, blank=False, db_column='goods_id')
    category_id = models.ForeignKey(Category,  blank=False, db_column='category_id')

    class Meta:
        db_table = 'goods_categories'
        unique_together = ('goods_id', 'category_id')



class Order(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    num_order = models.CharField(max_length=50, blank=False, db_column='num_order')
    adress = models.TextField(blank=False,  db_column='adress')
    use_name = num_items = models.CharField(max_length=40, blank=True,db_column='user_name')
    goods_id = models.ForeignKey(Goods, null=True, unique=False, blank=False, db_column='goods_id')
    user_id = models.ForeignKey(User, null=True, blank=False, db_column='user_id')
    telephones = models.CharField(max_length=40, blank=True,db_column='telephone')
    num_items = models.CharField(max_length=40, blank=True,db_column='num_items')
    city_id=models.ForeignKey(City,unique=False, blank=False, db_column='city_id')
    class Meta:
        db_table = 'order'
        #unique_together = ('goods_id', 'city_id')

        
class UserProfile(models.Model):
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User)

    
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'User profiles'

        
class Contacts (models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    post = models.CharField(max_length=50, blank=False, db_column='post')
    telephone = models.TextField(blank=False,  db_column='telephone')
    email= models.CharField(max_length=40, blank=True,db_column='email')
   
    class Meta:
        db_table = 'contacts'
        
class Basket(models.Model):
     id = models.AutoField(primary_key=True, db_column='id')
     date=models.DateTimeField('date')
     user_id = models.ForeignKey(User, null=True, blank=False, db_column='user_id')
     goods_id = models.ForeignKey(Goods, null=True, unique=False, blank=False, db_column='goods_id')
     num_items = models.CharField(max_length=40, blank=True,db_column='num_items')

     class Meta:
        db_table = 'basket'
     
     
     
