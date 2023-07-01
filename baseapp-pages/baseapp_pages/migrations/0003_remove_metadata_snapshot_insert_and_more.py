# Generated by Django 4.2.3 on 2023-12-19 02:42

import pgtrigger.compiler
import pgtrigger.migrations
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "baseapp_pages",
            "0002_metadataevent_pageevent_metadata_snapshot_insert_and_more",
        ),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name="metadata",
            name="snapshot_insert",
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name="metadata",
            name="snapshot_update",
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name="page",
            name="snapshot_insert",
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name="page",
            name="snapshot_update",
        ),
        migrations.AddField(
            model_name="metadataevent",
            name="pgh_operation",
            field=models.IntegerField(
                choices=[
                    (1, "Insert"),
                    (2, "Update"),
                    (3, "Delete"),
                    (4, "Insertorupdate"),
                ],
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="pageevent",
            name="pgh_operation",
            field=models.IntegerField(
                choices=[
                    (1, "Insert"),
                    (2, "Update"),
                    (3, "Delete"),
                    (4, "Insertorupdate"),
                ],
                null=True,
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="metadata",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "baseapp_pages_metadataevent" ("id", "language", "meta_description", "meta_og_image", "meta_og_type", "meta_robots", "meta_title", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "pgh_operation", "target_content_type_id", "target_object_id") VALUES (NEW."id", NEW."language", NEW."meta_description", NEW."meta_og_image", NEW."meta_og_type", NEW."meta_robots", NEW."meta_title", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", 1, NEW."target_content_type_id", NEW."target_object_id"); RETURN NULL;',
                    hash="822dc498b39e636433f02ed5c673356a93d7ab74",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_61603",
                    table="baseapp_pages_metadata",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="metadata",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition="WHEN (OLD.* IS DISTINCT FROM NEW.*)",
                    func='INSERT INTO "baseapp_pages_metadataevent" ("id", "language", "meta_description", "meta_og_image", "meta_og_type", "meta_robots", "meta_title", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "pgh_operation", "target_content_type_id", "target_object_id") VALUES (NEW."id", NEW."language", NEW."meta_description", NEW."meta_og_image", NEW."meta_og_type", NEW."meta_robots", NEW."meta_title", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", 2, NEW."target_content_type_id", NEW."target_object_id"); RETURN NULL;',
                    hash="656da07c81033ca0a7cdc2275898a4f798f8d35e",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_0e8cb",
                    table="baseapp_pages_metadata",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="metadata",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_delete",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "baseapp_pages_metadataevent" ("id", "language", "meta_description", "meta_og_image", "meta_og_type", "meta_robots", "meta_title", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "pgh_operation", "target_content_type_id", "target_object_id") VALUES (OLD."id", OLD."language", OLD."meta_description", OLD."meta_og_image", OLD."meta_og_type", OLD."meta_robots", OLD."meta_title", _pgh_attach_context(), NOW(), \'snapshot\', OLD."id", 3, OLD."target_content_type_id", OLD."target_object_id"); RETURN NULL;',
                    hash="3e63f4f8cd63e6c62cecf0e31d7af6e87ae9522e",
                    operation="DELETE",
                    pgid="pgtrigger_snapshot_delete_86b8d",
                    table="baseapp_pages_metadata",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="page",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "baseapp_pages_pageevent" ("body", "created", "id", "modified", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "pgh_operation", "title", "user_id") VALUES (NEW."body", NEW."created", NEW."id", NEW."modified", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", 1, NEW."title", NEW."user_id"); RETURN NULL;',
                    hash="c9265de2f4fb9766b137091e45901c728c37e083",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_f0c08",
                    table="baseapp_pages_page",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="page",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition="WHEN (OLD.* IS DISTINCT FROM NEW.*)",
                    func='INSERT INTO "baseapp_pages_pageevent" ("body", "created", "id", "modified", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "pgh_operation", "title", "user_id") VALUES (NEW."body", NEW."created", NEW."id", NEW."modified", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", 2, NEW."title", NEW."user_id"); RETURN NULL;',
                    hash="afae029350b9fef6c8b6235540b3ffc4a1da9eed",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_845c1",
                    table="baseapp_pages_page",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="page",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_delete",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "baseapp_pages_pageevent" ("body", "created", "id", "modified", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "pgh_operation", "title", "user_id") VALUES (OLD."body", OLD."created", OLD."id", OLD."modified", _pgh_attach_context(), NOW(), \'snapshot\', OLD."id", 3, OLD."title", OLD."user_id"); RETURN NULL;',
                    hash="8a09f2e49c06c0251905add5e9684ebba6178a99",
                    operation="DELETE",
                    pgid="pgtrigger_snapshot_delete_caf3a",
                    table="baseapp_pages_page",
                    when="AFTER",
                ),
            ),
        ),
    ]
