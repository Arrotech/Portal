import json

from utils.dummy import new_certificate, certificate_keys, certificate_name_restrictions,\
    update_certificate, update_certificate_keys, update_certificate_name_restrictions
from .base_test import BaseTest


class TestCertificates(BaseTest):
    """Test certificates endpoints."""

    def test_add_certificate(self):
        """Test that an admin can add a new certificate."""
        response1 = self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Certificate added successfully')
        assert response1.status_code == 201
        
    def test_add_certificate_keys(self):
        """Test that an admin cannot add a new certificate with invalid json keys."""
        response1 = self.client.post(
            '/api/v1/certificates', data=json.dumps(certificate_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Invalid certificate_name key')
        assert response1.status_code == 400

    def test_add_certificate_name_restrictions(self):
        """Test that an admin cannot add a new certificate with invalid certificate name."""
        response1 = self.client.post(
            '/api/v1/certificates', data=json.dumps(certificate_name_restrictions), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Invalid certificate name')
        assert response1.status_code == 400
        
    def test_get_all_certificates(self):
        """Test that a user can get all certificates."""
        response1 = self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.get(
            '/api/v1/certificates', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Certificates retrieved successfully')
        assert response2.status_code == 200
        
    def test_get_certificate_by_id(self):
        """Test that an admin can fetch certificate by id."""
        response1 = self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.get(
            '/api/v1/certificates/1', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Certificate retrieved successfully')
        assert response2.status_code == 200
        
    def test_get_non_existing_certificate_by_id(self):
        """Test that an admin cannot fetch non existing certificate by id."""
        response1 = self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.get(
            '/api/v1/certificates/10', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Certificate not found')
        assert response2.status_code == 404
        
    def test_update_certificate(self):
        """Test that an admin can update an existing certificate."""
        response1 = self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/certificates/1', data=json.dumps(update_certificate), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Certificate updated successfully')
        assert response2.status_code == 200
        
    def test_update_certificate_keys(self):
        """Test that an admin cannot update an existing certificate with invalid json keys."""
        response1 = self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/certificates/1', data=json.dumps(update_certificate_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Invalid certificate_name key')
        assert response2.status_code == 400
        
    def test_update_certificate_name_restrictions(self):
        """Test that an admin cannot update an existing certificate with invalid certificate name."""
        response1 = self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/certificates/1', data=json.dumps(update_certificate_name_restrictions), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Invalid certificate name')
        assert response2.status_code == 400
        
    def test_update_non_existing_certificate(self):
        """Test that an admin cannot update non existing certificate."""
        response1 = self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/certificates/10', data=json.dumps(update_certificate), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Certificate not found')
        assert response2.status_code == 404
        
    def test_delete_certificate(self):
        """Test that an admin can delete xisting certificate."""
        response1 = self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.delete(
            '/api/v1/certificates/1', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Certificate deleted successfully')
        assert response2.status_code == 200
        
    def test_delete_non_existing_certificate(self):
        """Test that an admin cannot delete non existing certificate."""
        response1 = self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.delete(
            '/api/v1/certificates/10', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Certificate not found')
        assert response2.status_code == 404
        
