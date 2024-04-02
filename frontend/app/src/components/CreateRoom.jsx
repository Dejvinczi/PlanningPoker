import React, { useState, useRef } from 'react';
import { useRouter } from 'next/router';
import { Toast } from 'primereact/toast';
import { Dialog } from 'primereact/dialog';
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import api from '@//api/root';

const CreateRoom = ({ visible, onHide }) => {
  const router = useRouter();
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});
  const toast = useRef(null);

  const showToast = (type, title, detail) => {
    toast.current.show({
      severity: type,
      summary: title,
      detail: detail,
      life: 3000,
    });
  };

  const handleSubmit = async () => {
    setErrors({});
    try {
      const response = await api.post('create-room', { password });
      showToast('success', 'Created the room', `Room: ${response.data.id}`);
      hideDialog();
      localStorage.setItem(
        response.data.id,
        JSON.stringify({ isAdmin: true, voterId: null }),
      );
      router.push({
        pathname: '/[roomId]',
        query: { roomId: response.data.id },
      });
    } catch (error) {
      if (error.response) {
        if (error.response.status === 400) setErrors(error.response.data);
        else showToast('error', 'Error', `Status ${error.response.status}`);
      } else showToast('error', 'Error', `Something went wrong`);

      return null;
    }
  };

  const hideDialog = () => {
    setPassword('');
    setErrors({});
    onHide();
  };

  return (
    <div>
      <Toast ref={toast} position='top-right' />
      <Dialog
        header='Create Room'
        visible={visible}
        onHide={hideDialog}
        modal
        position='top'
        draggable={false}
        footer={<Button label='Create' onClick={handleSubmit} />}
        style={{ width: '50vw' }}
      >
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <InputText
            id='password'
            placeholder='Password'
            type='password'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={errors.password ? 'p-invalid' : ''}
          />
          {errors.password && (
            <small className='p-error'>{errors.password}</small>
          )}
        </div>
      </Dialog>
    </div>
  );
};

export default CreateRoom;
