from django.db import models
from tenant_schemas.models import TenantMixin


# *********************************************************************************************************************
#  Welcome to DJANGO-TENANT-SCHEMAS documentation!
# *********************************************************************************************************************
# This application enables Django powered websites to have multiple tenants via PostgreSQL schemas. A vital feature for
# every Software-as-a-Service website.
# Django provides currently no simple way to support multiple tenants using the same project instance, even when only
# the data is different. Because we don’t want you running many copies of your project, you’ll be able to have:
#
# => Multiple customers running on the same instance
# *********************************************************************************************************************
# ==> Shared and Tenant-Specific data ==> that´s the option
# *********************************************************************************************************************
# => Tenant View-Routing
#
# What are schemas?
# A schema can be seen as a directory in an operating system, each directory (schema) with it’s own set of files
# (tables and objects). This allows the same table name and objects to be used in different schemas without conflict.
# For an accurate description on schemas, see PostgreSQL’s official documentation on schemas.
#
# Why schemas?
# There are typically three solutions for solving the multitenancy problem.
#
# Isolated Approach: Separate Databases. Each tenant has it’s own database.
# Semi Isolated Approach: Shared Database, Separate Schemas. One database for all tenants, but one schema per tenant.
# Shared Approach: Shared Database, Shared Schema. All tenants share the same database and schema. There is a main
# tenant-table, where all other tables have a foreign key pointing to.
# This application implements the second approach, which in our opinion, represents the ideal compromise between
# simplicity and performance.
#
# Simplicity: barely make any changes to your current code to support multitenancy. Plus, you only manage one database.
# Performance: make use of shared connections, buffers and memory.
# Each solution has it’s up and down sides, for a more in-depth discussion, see Microsoft’s excellent article on
# Multi-Tenant Data Architecture.
# *********************************************************************************************************************
class Cliente(TenantMixin):
    nome = models.CharField(max_length=100)
    pago_ate = models.DateField()
    em_teste = models.BooleanField(default=False)
    criado_em = models.DateField(auto_now_add=True)

    # default True, o schema será automaticamente criado e sincronizado quando for salvo.
    auto_create_schema = True

