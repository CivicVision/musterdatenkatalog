from crowdsourcing.forms import EvaluateWizardFirstStepForm,EvaluateWizardSecondStepForm,EvaluateWizardThirdStepForm
from musterdaten.models import Modeldataset
from musterdaten.test import TestCase
from musterdaten.tests.factories import (
    DatasetFactory,
    ModeldatasetFactory, Top3Factory, ModelsubjectFactory
)


class TestIndex(TestCase):
    def test_ok(self):
        self.get_check_200("crowdsourcing:index")


class TestEvaluate(TestCase):
    def test_ok(self):
        dataset = DatasetFactory()
        modeldataset = ModeldatasetFactory()
        modelsubject = ModelsubjectFactory()
        top3 = Top3Factory(dataset=dataset, modeldataset=modeldataset, pred=0.6)
        all_modelsubjects = dataset.top3_modelsubjects.all()
        top3_modeldatasets = dataset.top3_modeldatasets.all()
        all_modeldatasets = dataset.top3_modeldatasets.all()

        evaluate_wizard_first_step_form = EvaluateWizardFirstStepForm(
            initial={
                "dataset": dataset,
                "top3": all_modelsubjects,
            }
        )

        evaluate_wizard_second_step_form = EvaluateWizardSecondStepForm(
            initial=
            {
                "dataset": dataset,
                "top3_dataset": top3_modeldatasets,
            }

        )
        evaluate_wizard_third_step_form = EvaluateWizardThirdStepForm(
            initial=
            {
                "all_datasets": all_modeldatasets,
                "modelsubject": modelsubject,
            }

        )
        wizard_step_data = (
            {
                'dataset': evaluate_wizard_first_step_form,
                'evaluate_form_view-current_step': 'dataset',
            },
            {
                'dataset': evaluate_wizard_second_step_form,
                'evaluate_form_view-current_step': 'modelsubjects',
            },
            {
                'dataset': evaluate_wizard_third_step_form,
                'evaluate_form_view-current_step': 'modeldatasets',
            },
        )

        for data_step in wizard_step_data:
            response = self.post('crowdsourcing:evaluate', data=data_step)
            self.response_200(response)


    def test_failure(self):
        modeldataset = ModeldatasetFactory()
        data = {"dataset": "stri", "modeldataset": str(modeldataset.id)}

        response = self.post('crowdsourcing:evaluate', data=data)
        self.response_400(response)
