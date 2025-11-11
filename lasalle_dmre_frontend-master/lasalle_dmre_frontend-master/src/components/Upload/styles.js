import styled from 'styled-components';

import { v } from '../../styles/variables';


export const SUpload = styled.div`
    display: flex;
    //background: #31ab3c;
    width: 100%;
    height: calc(100% - (${v.mdSpacing} * 2));

    p {
        font-size: 30px;
        padding: 20px 0 30px 0;
        color: ${({theme}) => theme.text};
    }

    em {
        font-size: 20px;
        color: ${({theme}) => theme.text};
    }
`;