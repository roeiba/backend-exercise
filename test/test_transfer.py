import requests

base_url = "http://127.0.0.1:8000"


# test transfer student api
def test_transfer_student_api():
    """Test transfer student api"""
    student_id = 1
    student_name = "test_transfer_student_api"
    # build the student url
    student_url = "{}/students/{}".format(base_url, student_id)
    # build the request
    request_data = {
        "student_name": student_name,
        "student_id": student_id,
    }
    response = requests.post(
        student_url,
        json=request_data,
    )
    response.raise_for_status()
    # verify request data
    assert response.status_code == 200
    assert response.json() == request_data
