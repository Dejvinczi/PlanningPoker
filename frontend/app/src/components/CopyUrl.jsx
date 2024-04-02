import React, { useRef } from 'react';
import { Button } from 'primereact/button';
import { Toast } from 'primereact/toast';

const CopyUrl = ({ url, toastRef }) => {
  const toast = useRef(toastRef);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(url).then(() => {
      toast.current.show({
        severity: 'success',
        summary: 'Copied!',
        detail: 'Game URL copied to clipboard',
        life: 3000,
      });
    });
  };

  return (
    <div>
      <Toast ref={toast} />
      <Button
        label='Copy URL'
        onClick={copyToClipboard}
        className='p-button-success'
      />
    </div>
  );
};

export default CopyUrl;
