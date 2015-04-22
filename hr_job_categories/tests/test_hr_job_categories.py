# -*- coding:utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Savoir-faire Linux. All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.tests import common


class test_hr_job_categories(common.TransactionCase):
    def setUp(self):
        super(test_hr_job_categories, self).setUp()
        self.employee_model = self.registry('hr.employee')
        self.employee_categ_model = self.registry('hr.employee.category')
        self.user_model = self.registry('res.users')
        self.job_model = self.registry('hr.job')
        self.contract_model = self.registry('hr.contract')
        self.context = self.user_model.context_get(self.cr, self.uid)
        cr, uid, context = self.cr, self.uid, self.context

        #Create a employee
        self.employee_id = self.employee_model.create(
            cr, uid, {'name': 'Employee 1'}, context=context
        )
        
        #Create two employee categories
        self.categ_id = self.employee_categ_model.create(
            cr, uid, {'name': 'Category 1'}, context=context
        )
        self.categ_2_id = self.employee_categ_model.create(
            cr, uid, {'name': 'Category 2'}, context=context
        )
        
        #Create two jobs
        self.job_id = self.job_model.create(
            cr, uid, {'name': 'Job 1',
                      'category_ids': [(6, 0, [self.categ_id])]},
            context=context
        )
        self.job_2_id = self.job_model.create(
            cr, uid, {'name': 'Job 2',
                      'category_ids': [(6, 0, [self.categ_2_id])]},
            context=context
        )
        
        #Create one contract
        self.contract_id = self.contract_model.create(
            cr, uid, {
                'name': 'Contract 1',
                'employee_id': self.employee_id,
                'wage': 50000,
            }, context=context
        )

    def tearDown(self):
        cr, uid, context = self.cr, self.uid, self.context

        self.employee_categ_model.unlink(
            cr, uid, [self.categ_id, self.categ_2_id], context=context)
        self.job_model.unlink(
            cr, uid, [self.job_id, self.job_2_id], context=context)
        self.contract_model.unlink(
            cr, uid, [self.contract_id], context=context)
        self.employee_model.unlink(
            cr, uid, [self.employee_id], context=context)

        super(test_hr_job_categories, self).tearDown()

    def test_write_computes_with_normal_args(self):
        """
        Test that write method on hr_contract computes without error
        when the required data is given in parameter

        Check if the job categories are written to the employee.
        """
        cr, uid, context = self.cr, self.uid, self.context

        #Check if job categories are written to the employee
        self.contract_model.write(
            cr, uid, [self.contract_id], {
                'job_id': self.job_id,
            }, context=context
        )
        job = self.job_model.browse(
            self.cr, self.uid, [self.job_id], context=self.context
        )
        job_categ = [categ.id for categ in job.category_ids]
        employee = self.employee_model.browse(
            self.cr, self.uid, [self.employee_id], context=self.context
        )
        empl_categ = [categ.id for categ in employee.category_ids]
        
        self.assertTrue(all(x in empl_categ for x in job_categ))
        
        #Check if job2 categories are written to the employee
        self.contract_model.write(
            cr, uid, [self.contract_id], {
                'job_id': self.job_2_id,
            }, context=context
        )
        job = self.job_model.browse(
            self.cr, self.uid, [self.job_2_id], context=self.context
        )
        job_categ = [categ.id for categ in job.category_ids]
        employee = self.employee_model.browse(
            self.cr, self.uid, [self.employee_id], context=self.context
        )
        empl_categ = [categ.id for categ in employee.category_ids]
        
        self.assertTrue(all(x in empl_categ for x in job_categ))
        
