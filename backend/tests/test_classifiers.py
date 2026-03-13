from app.services.classifiers import ClassifierPipeline, RegionDelta


def test_classifier_pipeline_creates_change_items():
    pipeline = ClassifierPipeline()
    result = pipeline.run([RegionDelta("r1", 123.0, 0.0, (0, 0, 0))])
    assert len(result) == 1
    assert result[0]["change_id"] == "CHG-001"
    assert result[0]["change_type"] == "generic_region_change"
