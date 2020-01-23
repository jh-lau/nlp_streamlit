class QuestionPaser:
    '''构建实体节点'''

    @staticmethod
    def build_entity_dict(args):
        entity_dict = {}
        for arg, types in args.items():
            for _type in types:
                if _type in entity_dict:
                    entity_dict[_type].append(arg)
                else:
                    entity_dict[_type] = [arg]
        return entity_dict

    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entity_dict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'disease_symptom':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))

            elif question_type == 'disease_cause':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_accompany':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_not_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_do_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'food_not_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'food_do_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'disease_drug':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'disease_check':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'check_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('check'))

            elif question_type == 'disease_prevent':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_lasttime':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureway':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureprob':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_easyget':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            if sql:
                sql_['sql'] = sql
                sqls.append(sql_)

        return sqls

    @staticmethod
    def sql_transfer(question_type, entities):
        '''针对不同的问题，分开进行处理'''
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询疾病的原因
        if question_type == 'disease_cause':
            sql = [f"MATCH (m:Disease) where m.name = '{i}' return m.name, m.cause" for i in entities]

        # 查询疾病的防御措施
        elif question_type == 'disease_prevent':
            sql = [f"MATCH (m:Disease) where m.name = '{i}' return m.name, m.prevent" for i in entities]

        # 查询疾病的持续时间
        elif question_type == 'disease_lasttime':
            sql = [f"MATCH (m:Disease) where m.name = '{i}' return m.name, m.cure_lasttime" for i in entities]

        # 查询疾病的治愈概率
        elif question_type == 'disease_cureprob':
            sql = [f"MATCH (m:Disease) where m.name = '{i}' return m.name, m.cured_prob" for i in entities]

        # 查询疾病的治疗方式
        elif question_type == 'disease_cureway':
            sql = [f"MATCH (m:Disease) where m.name = '{i}' return m.name, m.cure_way" for i in entities]

        # 查询疾病的易发人群
        elif question_type == 'disease_easyget':
            sql = [f"MATCH (m:Disease) where m.name = '{i}' return m.name, m.easy_get" for i in entities]

        # 查询疾病的相关介绍
        elif question_type == 'disease_desc':
            sql = [f"MATCH (m:Disease) where m.name = '{i}' return m.name, m.desc" for i in entities]

        # 查询疾病有哪些症状
        elif question_type == 'disease_symptom':
            sql = [
                f"MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{i}' return m.name, r.name, n.name" for
                i in entities]

        # 查询症状会导致哪些疾病
        elif question_type == 'symptom_disease':
            sql = [
                f"MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{i}' return m.name, r.name, n.name" for
                i in entities]

        # 查询疾病的并发症
        elif question_type == 'disease_accompany':
            sql1 = [
                f"MATCH (m:Disease)-[r:accompany_with]->(n:Disease) where m.name = '{i}' return m.name, r.name, n.name"
                for i in entities]
            sql2 = [
                f"MATCH (m:Disease)-[r:accompany_with]->(n:Disease) where n.name = '{i}' return m.name, r.name, n.name"
                for i in entities]
            sql = sql1 + sql2
        # 查询疾病的忌口
        elif question_type == 'disease_not_food':
            sql = [f"MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{i}' return m.name, r.name, n.name" for i in
                   entities]

        # 查询疾病建议吃的东西
        elif question_type == 'disease_do_food':
            sql1 = [
                f"MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{i}' return m.name, r.name, n.name"
                for i in entities]
            sql2 = [
                f"MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where m.name = '{i}' return m.name, r.name, n.name" for
                i in entities]
            sql = sql1 + sql2

        # 已知忌口查疾病
        elif question_type == 'food_not_disease':
            sql = [f"MATCH (m:Disease)-[r:no_eat]->(n:Food) where n.name = '{i}' return m.name, r.name, n.name" for i in
                   entities]

        # 已知推荐查疾病
        elif question_type == 'food_do_disease':
            sql1 = [f"MATCH (m:Disease)-[r:do_eat]->(n:Food) where n.name = '{i}' return m.name, r.name, n.name"
                    for i in entities]
            sql2 = [f"MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where n.name = '{i}' return m.name, r.name, n.name"
                    for i in entities]
            sql = sql1 + sql2

        # 查询疾病常用药品－药品别名记得扩充
        elif question_type == 'disease_drug':
            sql1 = [f"MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{i}' return m.name, r.name, n.name"
                    for i in entities]
            sql2 = [f"MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where m.name = '{i}' return m.name, r.name, n.name"
                    for i in entities]
            sql = sql1 + sql2

        # 已知药品查询能够治疗的疾病
        elif question_type == 'drug_disease':
            sql1 = [f"MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{i}' return m.name, r.name, n.name"
                    for i in entities]
            sql2 = [f"MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where n.name = '{i}' return m.name, r.name, n.name"
                    for i in entities]
            sql = sql1 + sql2

        # 查询疾病应该进行的检查
        elif question_type == 'disease_check':
            sql = [f"MATCH (m:Disease)-[r:need_check]->(n:Check) where m.name = '{i}' return m.name, r.name, n.name" for
                   i in entities]

        # 已知检查查询疾病
        elif question_type == 'check_disease':
            sql = [f"MATCH (m:Disease)-[r:need_check]->(n:Check) where n.name = '{i}' return m.name, r.name, n.name" for
                   i in entities]

        return sql


if __name__ == '__main__':
    handler = QuestionPaser()