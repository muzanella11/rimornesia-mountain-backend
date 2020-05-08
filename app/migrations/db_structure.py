from app.config.migrations import MigrationsConfig

class DatabaseStructure(object):
    ACTION = MigrationsConfig().getAction()
    TABLES = {}

    def __init__(self):
        super(DatabaseStructure, self).__init__()

    def init_structure(self):
        self.indonesia_administrative()

        return self.TABLES

    def indonesia_administrative(self):
        self.TABLES['provinces'] = {
            'action': self.ACTION.get('create'),
            'command': (
                "CREATE TABLE IF NOT EXISTS `provinces` ("
                "   `id` char(2) COLLATE utf8_unicode_ci NOT NULL,"
                "   `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,"
                "   PRIMARY KEY (`id`)"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
            )
        }

        self.TABLES['regencies'] = {
            'action': self.ACTION.get('create'),
            'command': (
                "CREATE TABLE IF NOT EXISTS `regencies` ("
                "   `id` char(4) COLLATE utf8_unicode_ci NOT NULL,"
                "   `province_id` char(2) COLLATE utf8_unicode_ci NOT NULL,"
                "   `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,"
                "   PRIMARY KEY (`id`),"
                "   KEY `regencies_province_id_index` (`province_id`),"
                "   CONSTRAINT `regencies_province_id_foreign` FOREIGN KEY (`province_id`) REFERENCES `provinces` (`id`)"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
            )
        }

        self.TABLES['districts'] = {
            'action': self.ACTION.get('create'),
            'command': (
                "CREATE TABLE IF NOT EXISTS `districts` ("
                "   `id` char(7) COLLATE utf8_unicode_ci NOT NULL,"
                "   `regency_id` char(4) COLLATE utf8_unicode_ci NOT NULL,"
                "   `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,"
                "   PRIMARY KEY (`id`),"
                "   KEY `districts_id_index` (`regency_id`),"
                "   CONSTRAINT `districts_regency_id_foreign` FOREIGN KEY (`regency_id`) REFERENCES `regencies` (`id`)"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
            )
        }

        self.TABLES['villages'] = {
            'action': self.ACTION.get('create'),
            'command': (
                "CREATE TABLE IF NOT EXISTS `villages` ("
                "   `id` char(10) COLLATE utf8_unicode_ci NOT NULL,"
                "   `district_id` char(7) COLLATE utf8_unicode_ci NOT NULL,"
                "   `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,"
                "   PRIMARY KEY (`id`),"
                "   KEY `villages_district_id_index` (`district_id`),"
                "   CONSTRAINT `villages_district_id_foreign` FOREIGN KEY (`district_id`) REFERENCES `districts` (`id`)"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
            )
        }

    def indonesia_mountains (self):
        self.TABLES['mountains'] = {
            'action': self.ACTION.get('create'),
            'command': (
                "CREATE TABLE `mountains` ("
                " `id` int(100) NOT NULL AUTO_INCREMENT,"
                " `name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,"
                " `formatted_address` text COLLATE utf8_unicode_ci,"
                " `province_id` char(2) COLLATE utf8_unicode_ci DEFAULT '',"
                " `district_id` char(7) COLLATE utf8_unicode_ci DEFAULT '',"
                " `regency_id` char(4) COLLATE utf8_unicode_ci DEFAULT '',"
                " `village_id` char(10) COLLATE utf8_unicode_ci DEFAULT '',"
                " `location` text COLLATE utf8_unicode_ci,"
                " `raw_location` text COLLATE utf8_unicode_ci,"
                " PRIMARY KEY (`id`),"
                " KEY `mountains_province_id_index` (`province_id`),"
                " KEY `mountains_district_id_index` (`district_id`),"
                " KEY `mountains_regency_id_index` (`regency_id`),"
                " KEY `mountains_village_id_index` (`village_id`),"
                " CONSTRAINT `mountains_district_id_foreign` FOREIGN KEY (`district_id`) REFERENCES `districts` (`id`),"
                " CONSTRAINT `mountains_province_id_foreign` FOREIGN KEY (`province_id`) REFERENCES `provinces` (`id`),"
                " CONSTRAINT `mountains_regency_id_foreign` FOREIGN KEY (`regency_id`) REFERENCES `regencies` (`id`),"
                " CONSTRAINT `mountains_village_id_foreign` FOREIGN KEY (`village_id`) REFERENCES `villages` (`id`)"
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"
            )
        }

    # def rename_fields_salaries(self):
    #     action = {}

    #     action['salaries'] = {
    #         'action': self.ACTION.get('alter'),
    #         'command': (
    #             "ALTER TABLE salaries RENAME TO gaji"
    #         )
    #     }

    #     return action